import json
from pathlib import Path

from src.paper_trader import PaperBook, PaperPosition
from src.strategies.kalshi_common import evaluate_bundle

REAL_STATE = Path(__file__).resolve().parents[1] / "data" / "state.json"


def fin(result, value=None):
    if value is None:
        value = {"yes": "1.0000", "no": "0.0000"}.get(result)
    return {"status": "finalized", "result": result, "settlement_value_dollars": value}


def no_bundle(budget=10.0):
    return evaluate_bundle(
        strategy="buy_all_no", event_ticker="EV", key="EV", tickers=["A", "B"],
        sides=["no", "no"], ladders=[[(0.48, 50)], [(0.47, 50)]],
        min_payout_per_bundle=1.0, budget_usd=budget)


def test_no_position_pays_when_its_leg_loses():
    book = PaperBook(cash=100.0)
    pos, why = book.try_open(no_bundle(), None, "t0")
    assert why == "OPENED" and pos.sides == ["no", "no"]
    assert book.try_settle(pos, {"A": fin("yes"), "B": fin("no")}, "t1")
    assert pos.payout == pos.contracts * 1.0          # NO en A pierde, NO en B paga
    assert pos.realized_net > 0


def test_no_position_when_no_leg_wins_pays_k():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(no_bundle(), None, "t0")
    book.try_settle(pos, {"A": fin("no"), "B": fin("no")}, "t1")
    assert pos.payout == pos.contracts * 2.0


def test_no_position_cancelled_scalar():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(no_bundle(), None, "t0")
    book.try_settle(pos, {"A": fin("scalar", "0.3000"), "B": fin("scalar", "0.6000")}, "t1")
    assert abs(pos.payout - pos.contracts * (0.7 + 0.4)) < 1e-9


def test_mixed_yes_no_sides():
    book = PaperBook(cash=100.0)
    pos = PaperPosition(event_ticker="EV", legs=["B", "N"], contracts=5, cost=4.7,
                        fees=0.1, slippage=0.0, expected_net=0.2, opened_at="t0",
                        expected_close=None, sides=["yes", "no"])
    book.open.append(pos)
    # N implica B: si sale N, YES-B paga 1 y NO-N paga 0.
    book.try_settle(pos, {"B": fin("yes"), "N": fin("yes")}, "t1")
    assert pos.payout == 5.0


def test_capital_locked_until_settlement():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(no_bundle(), None, "t0")
    assert book.cash == 100.0 - pos.outlay and book.locked == pos.outlay
    assert not book.try_settle(pos, {"A": fin("yes")}, "t1")   # falta B
    assert book.locked == pos.outlay


def test_legacy_positions_without_sides_still_load_and_serialize_identically():
    legacy = {"cash": 90.0, "open": [{
        "event_ticker": "EV", "legs": ["A", "B"], "contracts": 10, "cost": 9.5,
        "fees": 0.36, "slippage": 0.02, "expected_net": 0.12, "opened_at": "t0",
        "expected_close": None, "closed_at": None, "payout": None}], "closed": []}
    book = PaperBook.from_dict(legacy, 100.0)
    assert book.open[0].sides is None
    assert book.to_dict() == legacy                  # mismo formato que kalshi_current
    assert book.try_settle(book.open[0], {"A": fin("yes"), "B": fin("no")}, "t1")
    assert book.closed[0].payout == 10.0             # YES por defecto


def test_real_kalshi_current_state_loads_unchanged():
    if not REAL_STATE.exists():
        return
    state = json.loads(REAL_STATE.read_text(encoding="utf-8"))
    book = PaperBook.from_dict(state.get("paper"), 100.0)
    assert book.to_dict() == state["paper"]
