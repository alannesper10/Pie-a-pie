import pytest

from lab.modules.liquidity import LiquidityProvision, apply_trades
from lab.modules.triangular import Triangular
from tests.lab_fixtures import TS, book, ctx, snap


# --- triangular --------------------------------------------------------------

def tri_books(eth_usdt_bid=2010.0, size=10.0):
    # USDT -> BTC (ask 50000) -> ETH (ETH/BTC ask 0.04) -> USDT (ETH/USDT bid)
    # tasa top = 2010 / (50000 * 0.04) = 1.005 (+0.5% bruto)
    return {"binance|BTC/USDT": book([(49990, size)], [(50000, size)]),
            "binance|ETH/BTC": book([(0.0399, size * 50)], [(0.04, size * 50)]),
            "binance|ETH/USDT": book([(eth_usdt_bid, size * 50)], [(eth_usdt_bid + 1, size * 50)])}


def tri_eval(b, after=None, **kw):
    m, c = Triangular(), ctx("triangular", **kw)
    s = snap(b, after)
    opps = {o.key: o for o in m.evaluate(s, c)}
    return m, c, s, opps


def test_triangle_gross_but_fees_kill_it():
    _, _, _, opps = tri_eval(tri_books(2005.0))        # +0.25% bruto < 3 x 0.1% de fees
    o = opps["binance|USDT->BTC->ETH->USDT"]
    assert o.observed["raw_gross_pct"] == pytest.approx(0.0025)
    assert o.reason == "NET_NEGATIVE_AFTER_COSTS"
    assert o.net_estimated_usd < 0 < o.gross_usd


def test_triangle_positive_and_executes():
    _, _, _, opps = tri_eval(tri_books(2020.0))       # +1% bruto
    o = opps["binance|USDT->BTC->ETH->USDT"]
    assert o.reason == "ESTIMATED_POSITIVE"
    assert o.costs["fees_3_patas"].usd > 0
    m, c, s, opps = tri_eval(tri_books(2020.0))
    o = opps["binance|USDT->BTC->ETH->USDT"]
    m.execute(o, s, c)
    assert o.reason == "FILLED" and o.sim["net_usd"] > 0
    assert o.sim["net_usd"] == pytest.approx(o.sim["final_usdt"] - o.size)


def test_triangle_disappears_or_partial_after_latency():
    after = tri_books(2020.0)
    after["binance|ETH/USDT"]["bids"] = [[1990.0, 500]]   # la última pata empeoró
    m, c, s, opps = tri_eval(tri_books(2020.0), after)
    o = opps["binance|USDT->BTC->ETH->USDT"]
    m.execute(o, s, c)
    assert o.sim["net_usd"] < 0                           # se ejecutó a precio peor


def test_triangle_leg_failure_values_leftover_conservatively():
    m, c, s, opps = tri_eval(tri_books(2020.0), fail=1.0)
    o = opps["binance|USDT->BTC->ETH->USDT"]
    m.execute(o, s, c)
    assert o.reason == "LEG_FAILED"
    assert o.sim["net_usd"] < 0          # quedó BTC y se vendió con comisión + penalidad


def test_no_triangle_when_book_missing():
    b = tri_books()
    del b["binance|ETH/BTC"]
    _, _, _, opps = tri_eval(b)
    assert "binance|USDT->BTC->ETH->USDT" not in opps


# --- provisión de liquidez: modelo de cola -----------------------------------

def order(price=100.0, queue=2.0, qty=1.0, active=1000):
    return {"price": price, "queue_ahead": queue, "remaining": qty, "qty": qty,
            "active_from_ms": active, "mid_at_quote": 100.05}


def tr(ts, price, amount, side):
    return {"ts": ts, "price": price, "amount": amount, "side": side}


def test_queue_ahead_must_be_consumed_first():
    o = order(queue=2.0)
    assert apply_trades(o, [tr(2000, 100.0, 1.5, "sell")], "bid") == 0
    assert o["queue_ahead"] == pytest.approx(0.5)
    assert apply_trades(o, [tr(3000, 100.0, 1.0, "sell")], "bid") == pytest.approx(0.5)


def test_trade_through_price_fills_fully():
    o = order(queue=50.0)
    assert apply_trades(o, [tr(2000, 99.9, 0.1, "sell")], "bid") == pytest.approx(1.0)


def test_trades_before_latency_and_wrong_side_are_ignored():
    o = order(queue=0.0, active=5000)
    assert apply_trades(o, [tr(4000, 100.0, 5, "sell")], "bid") == 0      # antes de existir
    assert apply_trades(o, [tr(6000, 100.0, 5, "buy")], "bid") == 0       # comprador no nos pega
    a = order(price=100.1, queue=0.0)
    assert apply_trades(a, [tr(2000, 100.1, 0.4, "buy")], "ask") == pytest.approx(0.4)


def test_liquidity_fill_markout_and_fees():
    m = LiquidityProvision(markets=(("binance", "BTC/USDT"),))
    c = ctx("liquidity_provision")
    b0 = {"binance|BTC/USDT": book([(100.0, 0.5)], [(100.2, 0.5)])}
    m.evaluate(snap(b0, tick=0), c)                       # coloca órdenes
    trades = {"binance|BTC/USDT": [tr(10**13, 99.9, 1.0, "sell")]}   # barre nuestro bid
    b1 = {"binance|BTC/USDT": book([(99.5, 1)], [(99.7, 1)])}         # el precio cayó
    fills = m.evaluate(snap(b1, tick=1, trades=trades), c)
    (f,) = [o for o in fills if o.reason == "FILL"]
    assert f.sim["side"] == "bid" and f.sim["fee_usd"] > 0
    b2 = {"binance|BTC/USDT": book([(99.0, 1)], [(99.2, 1)])}
    m.evaluate(snap(b2, tick=2, trades={"binance|BTC/USDT": []}), c)
    assert f.sim["markout_usd"] < 0                       # selección adversa: compramos y cayó
    assert f.sim["net_usd"] == pytest.approx(f.sim["spread_usd"] - f.sim["fee_usd"] + f.sim["markout_usd"])
    assert m.pop_updated() == [f]                         # se re-guarda con el markout


def test_inventory_limit_stops_quoting_bid():
    m = LiquidityProvision(markets=(("binance", "BTC/USDT"),))
    c = ctx("liquidity_provision")
    m.state["binance|BTC/USDT"] = {"orders": {}, "inv": 1.0, "cash": -100, "pending": [], "fills": 0}
    m.evaluate(snap({"binance|BTC/USDT": book([(100.0, 1)], [(100.2, 1)])}), c)
    assert set(m.state["binance|BTC/USDT"]["orders"]) == {"ask"}


def test_missing_trades_are_reported_not_invented():
    m = LiquidityProvision(markets=(("binance", "BTC/USDT"),))
    c = ctx("liquidity_provision")
    b = {"binance|BTC/USDT": book([(100.0, 1)], [(100.2, 1)])}
    m.evaluate(snap(b), c)
    out = m.evaluate(snap(b, tick=1, trades={}), c)
    assert out and all(o.reason == "NO_TRADES_DATA" for o in out)
