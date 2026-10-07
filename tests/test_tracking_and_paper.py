from src.event_arbitrage import evaluate_event_bundle, prefilter_event
from src.paper_trader import PaperBook, PaperPosition
from src.report import build_report
from src.tracking import (
    DURATION_FIELDS, NEAR_MISS_FIELDS, StreakTracker, append_csv, save_json,
)


def mk(ticker, ask, sub, **kw):
    return {"ticker": ticker, "market_type": "binary", "status": "active",
            "result": "", "yes_ask_dollars": str(ask), "yes_ask_size_fp": "100",
            "volume_24h_fp": "500", "yes_sub_title": sub, **kw}


def event(markets):
    return {"event_ticker": "EV", "title": "t", "mutually_exclusive": True,
            "markets": markets}


def executable_opp():
    pre = prefilter_event(event([mk("A", 0.3, "a"), mk("B", 0.3, "b"),
                                 mk("T", 0.3, "Tie")]), max_prelim_sum=10)[0]
    opp = evaluate_event_bundle(pre, [[(0.3, 50)]] * 3, fee_coefficient=0.07,
                                budget_usd=10)
    assert opp.executable
    return opp


# --- prefiltro estructural (lo que se cachea) ---

def test_structural_prefilter_ignores_prices():
    ms = [mk("A", 1.0, "a"), mk("B", 0.7, "b"), mk("T", 0.5, "Tie")]
    assert prefilter_event(event(ms))[1] == "LEG_WITHOUT_ASK"
    pre, reason = prefilter_event(event(ms), check_prices=False)
    assert reason == "OK"
    assert pre.prelim_sum == 2.2               # sin ask cuenta como 1.0


def test_structural_prefilter_still_requires_exhaustive():
    ms = [mk("A", 0.3, "a"), mk("O", 0.3, "Other")]
    assert prefilter_event(event(ms), check_prices=False)[1] == \
        "EXHAUSTIVENESS_UNCONFIRMED"


# --- paper: capital bloqueado hasta resolver ---

def test_open_locks_capital_without_crediting_profit():
    book = PaperBook(cash=100.0)
    opp = executable_opp()
    pos, why = book.try_open(opp, "2026-10-10T19:00:00+00:00", "t0")
    assert why == "OPENED"
    assert book.cash == 100.0 - pos.outlay
    assert book.locked == pos.outlay
    assert book.realized_net == 0
    assert book.try_open(opp, None, "t1") == (None, "ALREADY_OPEN")


def fin(result, value=None, status="finalized"):
    """Mercado liquidado con la forma que devuelve GET /events/{ticker}."""
    if value is None:
        value = {"yes": "1.0000", "no": "0.0000"}.get(result)
    return {"status": status, "result": result, "settlement_value_dollars": value}


def test_settle_waits_for_all_legs_then_pays():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(executable_opp(), None, "t0")
    pending = {"A": fin("no"), "B": fin("", status="active"),
               "T": fin("", status="active")}
    assert not book.try_settle(pos, pending, "t1")
    done = {"A": fin("no"), "B": fin("yes"), "T": fin("no")}
    assert book.try_settle(pos, done, "t2")
    assert pos.payout == pos.contracts
    assert pos.closed_at == "t2"
    assert book.locked == 0
    assert abs(book.cash - (100.0 + pos.realized_net)) < 1e-9
    assert pos.realized_net > 0


def test_settle_when_nothing_pays_loses_outlay():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(executable_opp(), None, "t0")
    book.try_settle(pos, {t: fin("no") for t in "ABT"}, "t1")
    assert pos.realized_net == -pos.outlay


def test_settle_waits_for_finalized_not_just_determined():
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(executable_opp(), None, "t0")
    determined = {"A": fin("no"), "B": fin("yes", status="determined"),
                  "T": fin("no")}
    assert not book.try_settle(pos, determined, "t1")
    assert book.try_settle(pos, {**determined, "B": fin("yes")}, "t2")


def test_cancelled_event_settles_scalar_values():
    # Caso real KXOSCARVIS-27: evento cancelado, cada pata liquidó "scalar".
    values = ["0.0800", "0.3000", "0.1000", "0.1600",
              "0.0900", "0.0200", "0.2300", "0.0200"]
    legs = [f"L{i}" for i in range(len(values))]
    book = PaperBook(cash=100.0)
    pos = PaperPosition(event_ticker="KXOSCARVIS-27", legs=legs, contracts=10,
                        cost=9.0, fees=0.2, slippage=0.0, expected_net=0.8,
                        opened_at="t0", expected_close=None)
    book.open.append(pos)
    assert book.try_settle(pos, {t: fin("scalar", v) for t, v in zip(legs, values)},
                           "t1")
    assert abs(pos.payout - 10.0) < 1e-9
    assert abs(pos.realized_net - 0.8) < 1e-9


def test_insufficient_cash():
    assert PaperBook(cash=1.0).try_open(executable_opp(), None, "t0") == \
        (None, "INSUFFICIENT_CASH")


def test_book_roundtrip():
    book = PaperBook(cash=100.0)
    book.try_open(executable_opp(), None, "t0")
    again = PaperBook.from_dict(book.to_dict(), 100.0)
    assert again.cash == book.cash and again.locked == book.locked


# --- rachas ---

T = ["2026-10-07T10:00:00+00:00", "2026-10-07T10:10:00+00:00",
     "2026-10-07T10:20:00+00:00", "2026-10-07T10:30:00+00:00",
     "2026-10-07T12:00:00+00:00"]


def test_streak_counts_consecutive_cycles():
    tr = StreakTracker(max_gap_min=15)
    assert tr.update(T[0], {"E"}, {"E"}) == []
    assert tr.update(T[1], {"E"}, {"E"}) == []
    closed = tr.update(T[2], set(), {"E"})
    assert closed == [{"event_ticker": "E", "first_seen": T[0],
                       "last_seen": T[1], "cycles": 2, "minutes": 10.0,
                       "end_reason": "EDGE_GONE"}]


def test_streak_not_observed_and_gap():
    tr = StreakTracker(max_gap_min=15)
    tr.update(T[0], {"E", "F"}, {"E", "F"})
    closed = tr.update(T[1], {"E"}, {"E"})
    assert [(c["event_ticker"], c["end_reason"]) for c in closed] == \
        [("F", "NOT_OBSERVED")]
    closed = tr.update(T[4], {"E"}, {"E"})       # 100 min sin ciclos
    assert closed[0]["end_reason"] == "GAP"
    assert tr.active["E"]["cycles"] == 1          # arranca una racha nueva


# --- reporte ---

def test_report(tmp_path):
    append_csv(tmp_path / "cycles.csv", ["timestamp", "ok"],
               {"timestamp": T[0], "ok": 1})
    append_csv(tmp_path / "cycles.csv", ["timestamp", "ok"],
               {"timestamp": T[1], "ok": 0})
    append_csv(tmp_path / "near_misses.csv", NEAR_MISS_FIELDS,
               {"event_ticker": "E", "executable": True})
    append_csv(tmp_path / "near_misses.csv", NEAR_MISS_FIELDS,
               {"event_ticker": "F", "executable": False})
    for cycles, minutes in ((1, 0), (3, 20), (2, 10)):
        append_csv(tmp_path / "opportunity_durations.csv", DURATION_FIELDS,
                   {"event_ticker": "E", "cycles": cycles, "minutes": minutes,
                    "end_reason": "EDGE_GONE"})
    book = PaperBook(cash=100.0)
    pos, _ = book.try_open(executable_opp(), None, "t0")
    book.try_settle(pos, {"A": fin("yes"), "B": fin("no"), "T": fin("no")}, "t1")
    save_json(tmp_path / "state.json", {"paper": book.to_dict(), "streaks": {}})

    out = build_report(tmp_path, 100.0, 10)
    assert "Ciclos: 2 (1 ok, 1 fallidos)" in out
    assert "Casi-aciertos (suma ask < 1,03): 2 registros" in out
    assert "Ejecutables: 1 registros" in out
    assert "promedio 2.0 | mediana 2.0" in out
    assert f"NETO TOTAL REALIZADO: US${pos.realized_net:+.2f}" in out
