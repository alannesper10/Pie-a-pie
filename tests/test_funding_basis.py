import math
import random

import pytest

from funding.basis import basis, basis_pct, basis_pnl, basis_stats
from funding.config import ASSUMED, VERIFIED, FundingConfig, Param, effective_fees
from funding.costs import (
    breakeven_periods, rebalance_cost_usd, round_trip_costs, slippage_vs_mid, walk_book,
)
from funding.funding import (
    annualize, expected_funding_pct, funding_payment, funding_stats,
    infer_interval_hours, trailing_mean,
)
from funding.paper import FundingPaperLedger, simulate_entry, simulate_exit
from funding.phase0 import backtest
from funding.risk import capital_required, liquidation_distance, short_liquidation_price
from funding.storage import Storage

H = 3_600_000
CFG = FundingConfig()


# --- funding ---------------------------------------------------------------

def test_funding_interval_inferred_from_history():
    assert infer_interval_hours([i * 8 * H for i in range(10)]) == 8
    assert infer_interval_hours([i * 1 * H for i in range(10)]) == 1
    assert infer_interval_hours([0, 8 * H]) is None       # datos insuficientes


def test_funding_interval_robust_to_one_gap():
    ts = [i * 8 * H for i in range(10)] + [100 * H]
    assert infer_interval_hours(ts) == 8


def test_expected_funding_and_annualize():
    assert math.isclose(expected_funding_pct(0.0001, 8, 7 * 24), 0.0021)
    assert math.isclose(annualize(0.0001, 8), 0.0001 * 3 * 365)
    assert trailing_mean([1, 2, 3, 4], 3) == 3


def test_funding_payment_sign_for_short():
    assert funding_payment(0.0001, 2, 50_000) == pytest.approx(10.0)    # cobra
    assert funding_payment(-0.0001, 2, 50_000) == pytest.approx(-10.0)  # paga


def test_funding_stats():
    s = funding_stats([0.0001, -0.0001, 0.0002, 0.0002], 8)
    assert s["pct_positive"] == 0.75 and s["mean"] == pytest.approx(0.0001)


# --- basis -----------------------------------------------------------------

def test_basis_and_pnl():
    assert basis(101, 100) == 1 and basis_pct(101, 100) == pytest.approx(0.01)
    # Entra con perp 1 arriba, sale con basis 0: gana 1 por unidad.
    assert basis_pnl(2, 100, 101, 110, 110) == pytest.approx(2.0)
    # Basis contrario (se amplía): pierde.
    assert basis_pnl(1, 100, 100, 100, 101) == pytest.approx(-1.0)
    assert basis_stats([0.01, -0.01])["mean_pct"] == 0


# --- costos ----------------------------------------------------------------

def test_round_trip_costs_include_every_component_with_status():
    c = round_trip_costs(CFG, "binance", spot_half_spread=0.0001, perp_half_spread=0.0002,
                         spot_depth_slip=0.0003, perp_depth_slip=0.0)
    names = set(c.items)
    assert {"fee_spot_entrada", "fee_spot_salida", "fee_perp_entrada", "fee_perp_salida",
            "spread_spot", "spread_perp", "slippage_profundidad_spot",
            "slippage_extra", "transferencias"} <= names
    st = c.statuses()
    assert st["fee_spot_entrada"] == ASSUMED and st["spread_spot"] == VERIFIED
    expected = (2 * 0.001 + 2 * 0.0005 + 2 * 0.0001 + 2 * 0.0002 + 2 * 0.0003
                + 4 * CFG.extra_slippage.value)
    assert c.total == pytest.approx(expected)


def test_costs_without_book_are_assumed():
    c = round_trip_costs(CFG, "okx")
    assert c.statuses()["spread_spot"] == ASSUMED


def test_effective_fees_take_the_higher_value():
    f = effective_fees(CFG.fees["okx"], 0.0015, 0.0005)
    assert f["spot_taker"].value == 0.0015 and f["spot_taker"].status == ASSUMED
    assert f["perp_taker"].value == 0.0005


def test_breakeven_and_positive_funding_is_not_profit():
    cost = round_trip_costs(CFG, "binance").total
    assert breakeven_periods(cost, 0.0) is None
    # 0.01% c/8h durante 7 días (21 períodos) no cubre ~0.38% de costos.
    assert expected_funding_pct(0.0001, 8, 7 * 24) < cost


def test_rebalance_cost():
    assert rebalance_cost_usd(100, CFG, "binance") == pytest.approx(
        100 * (0.001 + 0.0005 + 2 * CFG.extra_slippage.value))


# --- profundidad y fills parciales -----------------------------------------

def test_walk_book_partial_fill():
    assert walk_book([(100, 1), (101, 1)], 1.5) == (1.5, pytest.approx(100.3333333), 150.5)
    filled, _, _ = walk_book([(100, 0.4)], 1.0)
    assert filled == 0.4
    assert slippage_vs_mid([(100, 0.4)], 1.0, 99.5, "buy") is None


def test_entry_partial_perp_fill_unwinds_excess_spot():
    cfg = FundingConfig(leg_fail_prob=Param(0.0, ASSUMED, "test"))
    e = simulate_entry(spot_asks=[(100, 10)], spot_bids=[(99.9, 10)],
                       perp_bids=[(100, 0.6)], qty=1.0, cfg=cfg, exchange="binance",
                       rng=random.Random(1))
    assert e.status == "PARTIAL" and e.qty == pytest.approx(0.6)
    assert e.unmatched_qty == pytest.approx(0.4) and e.unmatched_cost > 0


def test_entry_second_leg_failure_unwinds_first():
    cfg = FundingConfig(leg_fail_prob=Param(1.0, ASSUMED, "test"))
    e = simulate_entry(spot_asks=[(100, 10)], spot_bids=[(99.8, 10)],
                       perp_bids=[(100, 10)], qty=1.0, cfg=cfg, exchange="binance",
                       rng=random.Random(1))
    assert e.status == "LEG_FAILED_UNWOUND" and e.qty == 0
    assert e.unmatched_cost > 0.2            # spread perdido + fee + penalidad
    led = FundingPaperLedger(cash=100.0)
    assert led.open_position(e, exchange="binance", asset="BTC", leverage=1, ts="t") is None
    assert led.cash < 100.0 and led.failed_entries == 1


def test_entry_full_fill_and_no_instant_fill_assumption():
    cfg = FundingConfig(leg_fail_prob=Param(0.0, ASSUMED, "test"))
    e = simulate_entry(spot_asks=[(100, 0.5), (101, 1)], spot_bids=[(99, 1)],
                       perp_bids=[(100.5, 0.3), (100, 1)], qty=1.0, cfg=cfg,
                       exchange="binance", rng=random.Random(1))
    assert e.status == "FILLED"
    assert e.spot.avg == pytest.approx(100.5)       # barrió 2 niveles
    assert e.perp.avg == pytest.approx(100.15)


def test_exit_insufficient_depth_is_penalized():
    s, p, fees, extra = simulate_exit(spot_bids=[(100, 0.5)], perp_asks=[(100, 0.5)],
                                      qty=1.0, cfg=CFG, exchange="binance")
    assert extra > 0 and fees > 0


# --- capital, funding, rebalanceo, liquidación -----------------------------

def _open(cfg=None, qty=0.4):
    cfg = cfg or FundingConfig(leg_fail_prob=Param(0.0, ASSUMED, "test"))
    e = simulate_entry(spot_asks=[(100, 10)], spot_bids=[(99.99, 10)],
                       perp_bids=[(100, 10)], qty=qty, cfg=cfg, exchange="binance",
                       rng=random.Random(1))
    led = FundingPaperLedger(cash=100.0)
    pos = led.open_position(e, exchange="binance", asset="BTC", leverage=1.0, ts="t0")
    return led, pos, cfg


def test_capital_locked_while_open():
    led, pos, _ = _open()
    assert pos.locked == pytest.approx(0.4 * 100 + 0.4 * 100)      # spot + margen 1x
    assert led.locked == pytest.approx(80.0)
    assert led.cash == pytest.approx(100 - 80 - pos.entry_fees)
    with pytest.raises(ValueError):
        _open(qty=0.6)                                             # 120 > 100


def test_funding_accrues_once_per_timestamp():
    led, pos, _ = _open()
    assert led.accrue_funding(pos, 0.0001, 100, 1000) == pytest.approx(0.004)
    assert led.accrue_funding(pos, 0.0001, 100, 1000) == 0.0       # duplicado ignorado
    led.accrue_funding(pos, -0.0002, 100, 2000)
    assert pos.funding_accrued == pytest.approx(0.004 - 0.008)


def test_rebalance_and_liquidation():
    led, pos, cfg = _open()
    assert led.check_risk(pos, 120, cfg) is None
    cash = led.cash
    assert led.check_risk(pos, 151, cfg) == "REBALANCE"            # pérdida > 50% margen
    assert pos.rebalances == 1 and led.cash < cash and pos.perp_ref == 151
    assert led.check_risk(pos, 151 * 2, cfg) == "LIQUIDATION"


def test_close_realizes_pnl_and_releases_capital():
    led, pos, cfg = _open()
    led.accrue_funding(pos, 0.0001, 100, 1)
    s, p, fees, extra = simulate_exit(spot_bids=[(100, 10)], perp_asks=[(100, 10)],
                                      qty=pos.qty, cfg=cfg, exchange="binance")
    net = led.close_position(pos, spot_exit=s, perp_exit=p, exit_fees=fees,
                             exit_extra=extra, ts="t1", reason="TEST")
    assert led.locked == 0 and not led.open
    assert led.cash == pytest.approx(100 + net)
    assert net == pytest.approx(0.004 - pos.entry_fees - fees)


def test_ledger_roundtrip():
    led, pos, _ = _open()
    again = FundingPaperLedger.from_dict(led.to_dict(), 100.0)
    assert again.locked == led.locked and again.cash == led.cash


def test_risk_helpers():
    assert capital_required(45, 1.0) == 90
    liq = short_liquidation_price(100, 1.0, 0.005)
    assert liq == pytest.approx(199.5)
    assert liquidation_distance(100, liq) == pytest.approx(0.995)


# --- storage ---------------------------------------------------------------

def test_storage_roundtrip_and_opportunity_lifecycle(tmp_path):
    st = Storage(tmp_path / "f.sqlite")
    st.save_funding("binance", "BTC", [(1, 0.0001), (2, 0.0002), (1, 0.0003)])
    assert st.load_funding("binance", "BTC") == [(1, 0.0003), (2, 0.0002)]
    st.save_prices("binance", "BTC", "spot", [(1, 100.0)])
    assert st.load_prices("binance", "BTC", "spot") == [(1, 100.0)]
    oid = st.open_opportunity("okx", "BTC", "t0", 0.001, 45, {"x": 1})
    assert st.open_opportunity_id("okx", "BTC") == oid
    st.update_opportunity(oid, 0.002, 45)
    st.close_opportunity(oid, "t1")                                # desaparece
    assert st.open_opportunity_id("okx", "BTC") is None
    row = st.db.execute("SELECT snapshots, max_expected_net_pct, closed_at "
                        "FROM opportunities").fetchone()
    assert row == (2, 0.002, "t1")
    st.log_error("t", "bybit", "x", "boom")
    st.put("k", {"a": 1})
    assert st.get("k") == {"a": 1} and st.count("errors") == 1
    st.close()


# --- backtest (sin mirar el futuro) ----------------------------------------

def _series(n_funding, rate, price=100.0):
    fund = [(i * 8 * H, rate) for i in range(n_funding)]
    hours = {h * H: price for h in range(n_funding * 8 + 10)}
    return fund, hours


def test_backtest_never_enters_when_costs_exceed_expected_funding():
    fund, px = _series(90, 0.0001)                  # 0.01% c/8h, tope típico
    cfg = FundingConfig(horizon_days=7)
    bt = backtest(fund, px, px, px, interval_hours=8, round_trip_cost_pct=0.0038,
                  cfg=cfg, exchange="binance", notional=45)
    assert bt.decisions > 0 and bt.ex_ante_positive == 0 and bt.trades == []


def test_backtest_enters_after_latency_bar_and_collects_funding():
    fund, px = _series(60, 0.001)                   # funding alto: 0.1% c/8h
    cfg = FundingConfig(horizon_days=7, max_hold_days=5)
    bt = backtest(fund, px, px, px, interval_hours=8, round_trip_cost_pct=0.004,
                  cfg=cfg, exchange="binance", notional=45)
    t = bt.trades[0]
    decision_ts = fund[cfg.trailing_periods - 1][0]
    assert t.entry_ts == decision_ts + H            # 1 barra de latencia
    assert t.funding_usd > 0 and t.net_usd == pytest.approx(
        t.funding_usd + t.basis_pnl_usd - t.costs_usd - t.rebalance_costs_usd)


def test_backtest_does_not_use_future_rates():
    # Funding negativo hasta la mitad y muy positivo después: la decisión en la
    # primera mitad no puede "ver" lo que viene.
    fund = [(i * 8 * H, -0.0005 if i < 30 else 0.002) for i in range(60)]
    px = {h * H: 100.0 for h in range(60 * 8 + 10)}
    bt = backtest(fund, px, px, px, interval_hours=8, round_trip_cost_pct=0.004,
                  cfg=FundingConfig(), exchange="binance", notional=45)
    assert all(t.entry_ts > 30 * 8 * H for t in bt.trades)
