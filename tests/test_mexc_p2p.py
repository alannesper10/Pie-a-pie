"""MEXC P2P: precios anómalos se excluyen en el filtro plausible; límites y costos aplicados."""

import pytest

from lab.research import mexc_p2p as mx


def ad(price, country="AR", mtype="merchant", done=50, rate="1.0000", mn=10_000, mx_=1_000_000, qty=10_000):
    return {"price": price, "country": country, "merchant_type": mtype, "done_30d": done,
            "complete_rate_30d": rate, "min_ars": mn, "max_ars": mx_, "qty": qty, "nick": "n"}


def snap(sells, buys, bid=1614.0, ask=1614.2):
    return {"ts": "t", "binance_usdtars": {"data": {"bids": [[str(bid), "100000"]], "asks": [[str(ask), "1"]]}},
            "mexc_p2p_sell": {"data": sells}, "mexc_p2p_buy": {"data": buys}}


def test_anomalous_discount_is_excluded_by_plausible_filter():
    s = snap([ad(1480.0), ad(1611.0)], [ad(1650.0, country="PH", mtype="normal"), ad(1607.0)])
    anyr = mx.evaluate(s, flt="any")
    assert anyr["buy_price"] == 1480.0 and anyr["m1_sell_price"] == 1650.0
    assert anyr["m1_net_pct"] == pytest.approx((1650 / 1480 - 1) * 100)
    pl = mx.evaluate(s, flt="plausible")
    assert pl["buy_price"] == 1611.0 and pl["m1_sell_price"] == 1607.0
    assert pl["m1_net_pct"] < 0


def test_limits_fees_and_withdrawal():
    s = snap([ad(1600.0, mn=200_000)], [ad(1607.0)])
    assert mx.evaluate(s, ars=150_000) is None                # monto menor al mínimo del anuncio
    s = snap([ad(1600.0)], [ad(1610.0)])
    r = mx.evaluate(s, ars=160_000, p2p_fee=0.002, withdraw_usdt=1.0)
    usdt = 100 * 0.998
    assert r["m1_net_pct"] == pytest.approx((usdt * 1610 * 0.998 / 160_000 - 1) * 100)
    assert r["m2_net_pct_before_ars_withdraw"] == pytest.approx(((usdt - 1) * 1614 * 0.999 / 160_000 - 1) * 100)
