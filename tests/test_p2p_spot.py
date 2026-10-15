"""P2P -> libro de Binance: ciclos secuenciales, venta en la captura posterior y costos."""

import pytest

from lab.research import p2p_spot as ps


def snap(ts, bid, ads, qty=1e6):
    return {"ts": ts, "binance_usdtars": {"data": {"bids": [[str(bid), str(qty)]], "asks": [[str(bid + 0.1), "1"]]}},
            "p2p_usdt_ars_buy": {"data": ads}}


def ad(price, user_type="merchant", methods=("MercadoPagoNew",), mn=10_000, mx=1e9, qty=1e6, om=500, fr=1.0):
    return {"price": price, "user_type": user_type, "methods": list(methods), "min_ars": mn, "max_ars": mx,
            "qty": qty, "orders_month": om, "finish_rate": fr}


def test_sells_at_later_capture_with_real_price_move_and_fees():
    s = [snap("2026-10-15T15:00:00+00:00", 1615, [ad(1610)]),
         snap("2026-10-15T15:01:00+00:00", 1615, [ad(1610)]),
         snap("2026-10-15T15:05:00+00:00", 1612, [ad(1610)])]      # el precio cayó antes de vender
    pol = ps.Policy(capital_ars=161_000, pay_s=180, release_s=60, min_edge=0.0)
    c = ps.run(s, pol, ps.Costs(withdraw_s=0))
    assert c[0]["status"] == "OK" and c[0]["sold_ts"] == s[2]["ts"]
    usdt = 161_000 / 1610
    assert c[0]["net_ars"] == pytest.approx(usdt * 1612 * 0.999 - 161_000)
    assert c[0]["price_move_pct"] == pytest.approx((1612 / 1615 - 1) * 100)


def test_cycles_do_not_overlap_until_capital_returns():
    s = [snap(f"2026-10-15T15:{m:02d}:00+00:00", 1615, [ad(1600)]) for m in range(0, 30)]
    pol = ps.Policy(capital_ars=100_000, pay_s=60, release_s=60, min_edge=0.0)
    c = ps.run(s, pol, ps.Costs(withdraw_s=10 * 60))
    ok = [x for x in c if x["status"] == "OK"]
    # cada ciclo: 2 min hasta vender + 10 min de retiro -> no más de uno cada 12 min
    assert len(ok) == 3
    assert ps._ts(ok[1]["ts"]) >= ps._ts(ok[0]["sold_ts"])


def test_filters_counterparty_methods_limits_and_min_edge():
    ads = [ad(1600, user_type="user", om=5, fr=0.9),                 # particular sin historial
           ad(1601, methods=("Zinli",)),                               # medio no usable
           ad(1602, mn=2_000_000),                                     # mínimo mayor al capital
           ad(1614.9)]                                                 # margen < umbral
    s = [snap("2026-10-15T15:00:00+00:00", 1615, ads), snap("2026-10-15T15:05:00+00:00", 1615, ads)]
    assert ps.run(s, ps.Policy(capital_ars=500_000, counterparty="merchant"), ps.Costs()) == []
    c = ps.run(s, ps.Policy(capital_ars=500_000, counterparty="any", min_edge=0.0), ps.Costs(withdraw_s=0))
    assert c[0]["ad_price"] == 1600


def test_unknown_withdrawal_fee_scenario_can_erase_margin():
    s = [snap("2026-10-15T15:00:00+00:00", 1615, [ad(1612)]), snap("2026-10-15T15:05:00+00:00", 1615, [ad(1612)])]
    pol = ps.Policy(capital_ars=161_200, min_edge=-1)
    free = ps.run(s, pol, ps.Costs(withdraw_s=0))[0]["net_pct"]
    paid = ps.run(s, pol, ps.Costs(withdraw_s=0, ars_withdraw_pct=0.005))[0]["net_pct"]
    assert free > 0 > paid


def test_gap_in_data_is_not_filled():
    s = [snap("2026-10-15T15:00:00+00:00", 1615, [ad(1600)]), snap("2026-10-15T16:00:00+00:00", 1615, [ad(1600)])]
    c = ps.run(s, ps.Policy(min_edge=0.0), ps.Costs())
    assert c[0]["status"] == "SIN_DATOS"


def test_book_depth_limits_sale():
    s = [snap("2026-10-15T15:00:00+00:00", 1615, [ad(1600)], qty=10),
         snap("2026-10-15T15:05:00+00:00", 1615, [ad(1600)], qty=10)]
    c = ps.run(s, ps.Policy(capital_ars=1_600_000, min_edge=0.0), ps.Costs())
    assert c[0]["status"] == "SIN_PROFUNDIDAD"
