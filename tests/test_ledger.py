"""Libro central: un mismo dólar no puede estar en dos estrategias; lo comprometido no se reasigna."""

import pytest

from lab.ledger import CentralLedger, LedgerError


def led(tmp_path=None):
    l = CentralLedger(1000.0, tmp_path / "ledger.jsonl" if tmp_path else None)
    l.register("a")
    l.register("b")
    return l


def test_capital_cannot_be_allocated_twice():
    l = led()
    l.allocate("a", 700)
    with pytest.raises(LedgerError):
        l.allocate("b", 400)                 # solo quedan 300
    l.allocate("b", 300)
    assert l.unallocated == pytest.approx(0)


def test_committed_capital_is_not_reassignable():
    l = led()
    l.allocate("a", 500)
    l.commit("a", "t1", 400, "2026-10-16T12:00")
    with pytest.raises(LedgerError):
        l.deallocate("a", 200)               # solo 100 disponibles
    with pytest.raises(LedgerError):
        l.commit("a", "t2", 150, "2026-10-16T12:01")
    with pytest.raises(LedgerError):
        l.commit("a", "t1", 10, "2026-10-16T12:01")   # id repetido
    l.deallocate("a", 100)
    assert l.accounts["a"].available == pytest.approx(0)


def test_release_books_net_pnl_in_strategy_and_total():
    l = led()
    l.allocate("a", 500)
    l.commit("a", "t1", 400, "t0")
    l.release("t1", gross_pnl=10.0, costs={"spot_taker": 0.4, "withdraw": 1.0}, ts="t1")
    r = l.report()
    s = r["strategies"]["a"]
    assert s["realized_net"] == pytest.approx(8.6) and s["costs"] == pytest.approx(1.4)
    assert s["allocated"] == pytest.approx(508.6) and s["committed"] == 0
    assert r["equity"] == pytest.approx(1008.6) and r["net_return_pct"] == pytest.approx(0.86)
    assert s["return_on_used_pct"] == pytest.approx(8.6 / 400 * 100)
    assert s["costs_share_of_gross"] == pytest.approx(0.14)


def test_losses_drawdown_and_unrealized_not_counted_as_realized():
    l = led()
    l.allocate("a", 100)
    for i, g in enumerate([5.0, -15.0, 2.0]):
        l.commit("a", f"t{i}", 50, "x")
        l.release(f"t{i}", g, {}, "y")
    l.mark("a", 30.0, "z")
    r = l.report()
    s = r["strategies"]["a"]
    assert s["realized_net"] == pytest.approx(-8.0) and r["equity"] == pytest.approx(992.0)
    assert s["unrealized"] == 30.0                         # se informa aparte, no suma al patrimonio
    assert s["max_drawdown_pct"] == pytest.approx((90 / 105 - 1) * 100)
    assert s["win_rate"] == pytest.approx(2 / 3) and s["expectancy"] == pytest.approx(-8 / 3)


def test_event_log_replays_to_same_state(tmp_path):
    l = led(tmp_path)
    l.allocate("a", 600, "evidencia X")
    l.commit("a", "t1", 100, "t0", {"venue": "binance"})
    l.release("t1", 3.0, {"fee": 0.1}, "t1")
    l.set_status("a", "VALIDACION", "30 ciclos")
    r1 = l.report()
    r2 = CentralLedger.replay(tmp_path / "ledger.jsonl").report()
    assert r1 == r2
