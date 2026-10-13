import pytest

import lab.fees
from lab.core import (
    ASSUMED, Cost, LiquidityRegistry, Opportunity, StrategyLedger, cost_total, make_rng,
    scale_costs, walk, walk_quote,
)
from lab.modules.cross_exchange import CrossExchange
from tests.lab_fixtures import TS, TS2, book, ctx, snap


# --- motor común -------------------------------------------------------------

def test_walk_and_walk_quote_partial():
    assert walk([(100, 1), (101, 1)], 1.5) == (1.5, pytest.approx(150.5), [(100, 1), (101, 0.5)])
    base, spent, fills = walk_quote([(100, 1), (200, 1)], 150)
    assert base == pytest.approx(1.25) and spent == pytest.approx(150)


def test_registry_prevents_double_use_of_liquidity():
    r = LiquidityRegistry()
    lv = [(100.0, 1.0), (101.0, 2.0)]
    r.claim("binance", "BTC/USDT", "asks", [(100.0, 0.6)])
    assert r.available("binance", "BTC/USDT", "asks", lv) == [(100.0, pytest.approx(0.4)), (101.0, 2.0)]
    r.claim("binance", "BTC/USDT", "asks", [(100.0, 0.4)])
    assert r.available("binance", "BTC/USDT", "asks", lv) == [(101.0, 2.0)]
    assert r.available("okx", "BTC/USDT", "asks", lv) == lv       # otro venue: intacto


def test_ledger_capital_is_separate_and_locked():
    a, b = StrategyLedger("a", 100), StrategyLedger("b", 100)
    a.commit(60)
    assert a.cash == 40 and a.locked == 60 and b.cash == 100
    with pytest.raises(ValueError):
        a.commit(50)
    a.release(60, 1.5, {"k": 1})
    assert a.cash == 101.5 and a.locked == 0 and a.peak_locked == 60 and b.realized == 0


def test_opportunity_net_and_stress():
    o = Opportunity("s", "k", 0, TS, ["v"], ["x"], {}, gross_usd=1.0, capital_usd=50,
                    costs={"fee": Cost(0.4, ASSUMED, "t"), "x": Cost(0.2, ASSUMED, "t")})
    assert o.net_estimated_usd == pytest.approx(0.4)
    assert o.net_estimated_pct == pytest.approx(0.008)
    assert cost_total(o.costs) == pytest.approx(0.6) and scale_costs(o.costs, 2) == pytest.approx(1.2)


def test_rng_is_reproducible_per_seed():
    assert make_rng(7, "s", 3).random() == make_rng(7, "s", 3).random()
    assert make_rng(7, "s", 3).random() != make_rng(8, "s", 3).random()


# --- cross_exchange ----------------------------------------------------------

@pytest.fixture
def no_rebalance(monkeypatch):
    """Aísla la mecánica de ejecución del costo de rebalanceo supuesto."""
    monkeypatch.setitem(lab.fees.WITHDRAW_USD, "BTC", 0.0)

def books(ask_a=100.0, bid_b=101.0, size=1.0, ts_b=TS2, extra=None):
    b = {"binance|BTC/USDT": book([(99.9, 5)], [(ask_a, size)]),
         "okx|BTC/USDT": book([(bid_b, size)], [(bid_b + 0.1, 5)], ts=ts_b)}
    b.update(extra or {})
    return b


def evaluate(b, after=None, **kw):
    m = CrossExchange(symbols=("BTC/USDT",))
    c = ctx("cross_exchange", **kw)
    s = snap(b, after)
    opps = [o for o in m.evaluate(s, c) if o.venues == ["binance", "okx"]]
    return m, c, s, opps


def test_spread_must_beat_fees_both_sides():
    _, _, _, (o,) = evaluate(books(100.0, 100.15))      # 0.15% < 0.2% de fees
    assert o.reason == "NO_EDGE_AFTER_FEES" and o.net_estimated_usd < 0


def test_regression_no_edge_reference_uses_real_size_not_one_unit():
    # Bug: la referencia sin edge usaba 1 BTC (US$83.000) y daba -US$157.
    b = {"binance|BTC/USDT": book([(83000, 5)], [(83000.0, 5)]),
         "okx|BTC/USDT": book([(83005.0, 5)], [(83006, 5)], ts=TS2)}
    _, _, _, opps = evaluate(b)
    (o,) = [x for x in opps]
    assert o.reason == "NO_EDGE_AFTER_FEES"
    assert o.capital_usd <= 50 + 1e-6 and o.net_estimated_usd > -2


def test_estimated_positive_counts_all_costs(no_rebalance):
    _, _, _, (o,) = evaluate(books(100.0, 101.0, size=0.2))
    assert o.reason == "ESTIMATED_POSITIVE"
    assert o.size == pytest.approx(0.2) and o.capital_usd == pytest.approx(40)
    assert set(o.costs) >= {"fee_compra_binance", "fee_venta_okx", "rebalanceo"}
    assert o.costs["rebalanceo"].status == ASSUMED
    assert o.net_estimated_usd == pytest.approx(0.2 * 1.0 - 0.02 - 0.0202)


def test_rebalance_cost_kills_small_capital():
    # Con US$100 (~US$50 por operación) el retiro de BTC amortizado (US$1 por
    # operación) supera un 1% de diferencia: no hay neto positivo.
    _, _, _, (o,) = evaluate(books(100.0, 101.0, size=0.2))
    assert o.costs["rebalanceo"].usd == pytest.approx(1.0)
    assert o.reason == "NET_NEGATIVE_AFTER_COSTS"


def test_implausible_spread_is_suspicious():
    _, _, _, (o,) = evaluate(books(100.0, 103.0, size=0.2))
    assert o.reason == "SUSPICIOUS_SPREAD_CHECK_TRANSFERS"


def test_size_capped_by_capital(no_rebalance):
    _, _, _, (o,) = evaluate(books(100.0, 101.0, size=10.0))
    assert o.capital_usd <= 50 + 1e-9                      # 50% del capital por operación


def test_stale_books_are_rejected():
    _, _, _, (o,) = evaluate(books(100.0, 103.0, ts_b="2026-10-09T12:00:05.000+00:00"))
    assert o.reason == "STALE_BOOKS"


def test_min_size_rejected(no_rebalance):
    m = {"okx|BTC/USDT": {"min_amount": 1.0}}
    mod = CrossExchange(symbols=("BTC/USDT",))
    c = ctx("cross_exchange")
    (o,) = [x for x in mod.evaluate(snap(books(100.0, 101.0, size=0.2), markets=m), c)
            if x.venues == ["binance", "okx"]]
    assert o.reason == "MIN_SIZE_okx"


def test_opportunity_disappears_after_latency(no_rebalance):
    after = books(101.5, 100.5, size=0.2)               # el spread se cerró
    m, c, s, (o,) = evaluate(books(100.0, 101.0, size=0.2), after)
    m.execute(o, s, c)
    assert o.reason == "DISAPPEARED" and o.decision == "REJECTED"
    assert o.sim["net_usd"] == 0 and c.ledger.realized == 0


def test_partial_fill_unwinds_excess_with_cost(no_rebalance):
    after = books(100.0, 101.0, size=0.2)
    after["okx|BTC/USDT"]["bids"] = [[101.0, 0.05]]       # en B quedó poca profundidad
    m, c, s, (o,) = evaluate(books(100.0, 101.0, size=0.2), after)
    m.execute(o, s, c)
    assert o.reason == "PARTIAL" and o.sim["matched"] == pytest.approx(0.05)
    assert o.sim["unwind_usd"] > 0


def test_leg_failure_costs_money(no_rebalance):
    m, c, s, (o,) = evaluate(books(100.0, 101.0, size=0.2), fail=1.0)
    m.execute(o, s, c)
    assert o.reason == "LEG_FAILED" and o.sim["net_usd"] < 0 and c.ledger.realized < 0


def test_liquidity_used_by_one_opportunity_is_not_reused(no_rebalance):
    reg = LiquidityRegistry()
    b = books(100.0, 101.0, size=0.2)
    m = CrossExchange(symbols=("BTC/USDT",))
    c1 = ctx("cross_exchange", registry=reg)
    (o1,) = [x for x in m.evaluate(snap(b), c1) if x.venues == ["binance", "okx"]]
    m.execute(o1, snap(b), c1)
    c2 = ctx("otra", registry=reg)
    (o2,) = [x for x in m.evaluate(snap(b), c2) if x.venues == ["binance", "okx"]]
    m.execute(o2, snap(b), c2)
    assert o1.sim["matched"] == pytest.approx(0.2)
    assert o2.reason == "DISAPPEARED"                     # ya no había liquidez


def test_execution_is_reproducible_with_seed(no_rebalance):
    res = []
    for _ in range(2):
        m, c, s, (o,) = evaluate(books(100.0, 101.0, size=0.2), seed=42, fail=0.5)
        m.execute(o, s, c)
        res.append((o.reason, o.sim["net_usd"]))
    assert res[0] == res[1]
