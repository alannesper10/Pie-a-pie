from datetime import datetime, timezone

from src import notify
from src.paper_trader import PaperBook
from src.strategies.kalshi_common import (
    OPPORTUNITY_FIELDS, PAPER_FIELDS, STRATEGY_CYCLE_FIELDS,
)
from src.tracking import CYCLE_FIELDS, NEAR_MISS_FIELDS, append_csv, save_json

NOW = "2026-10-07T12:00:00+00:00"
SINCE = datetime.fromisoformat("2026-10-07T11:59:00+00:00")


def strat(d, name, executable=False, ok=1, error="", opened=False, near=True):
    sd = d / "strategies" / name
    append_csv(sd / "cycles.csv", STRATEGY_CYCLE_FIELDS,
               {"timestamp": NOW, "strategy": name, "ok": ok, "error": error})
    if near:
        append_csv(sd / "opportunities.csv", OPPORTUNITY_FIELDS, {
            "timestamp": NOW, "strategy": name, "event_ticker": "EV", "key": "EV-A|EV-B",
            "contracts": 10 if executable else 0, "net_profit": 0.25 if executable else -0.01,
            "max_contracts_available": 10 if executable else 0,
            "executable": executable, "reason": "NET_EDGE_OK" if executable else "X"})
    if opened:
        append_csv(sd / "paper_trades.csv", PAPER_FIELDS, {
            "timestamp": NOW, "action": "OPEN", "event_ticker": "EV",
            "expected_net": 0.25, "cash_after": 90.3})
    save_json(sd / "state.json", {"paper": PaperBook(cash=90.3 if opened else 100.0).to_dict(),
                                  "streaks": {}})


def current_ok(d):
    append_csv(d / "cycles.csv", CYCLE_FIELDS, {"timestamp": NOW, "ok": 1})
    append_csv(d / "near_misses.csv", NEAR_MISS_FIELDS, {
        "timestamp": NOW, "event_ticker": "K", "ask_sum": 0.99, "n_legs": 3,
        "est_net": -0.04, "executable": False, "reason": "NO_POSITIVE_MARGINAL_EDGE"})


def test_near_misses_of_any_strategy_do_not_notify(tmp_path):
    current_ok(tmp_path)
    strat(tmp_path, "buy_all_no")
    strat(tmp_path, "strike_inconsistency")
    assert notify.compose_cycle_message(tmp_path, SINCE) is None


def test_single_strategy_executable_is_tagged(tmp_path):
    current_ok(tmp_path)
    strat(tmp_path, "buy_all_no", executable=True, opened=True)
    title, body, prio, _ = notify.compose_cycle_message(tmp_path, SINCE)
    assert title == "[BUY_ALL_NO] Pie a pie: novedad"
    assert "Ejecutable: EV-A|EV-B, 10 contratos, neto US$+0.25" in body
    assert "Paper abierta: EV" in body and "Caja: US$90.30" in body
    assert prio == 4


def test_multiple_sections_in_one_message(tmp_path):
    append_csv(tmp_path / "cycles.csv", CYCLE_FIELDS,
               {"timestamp": NOW, "ok": 0, "error": "ConnectionError('x')"})
    strat(tmp_path, "strike_inconsistency", executable=True)
    title, body, _, tags = notify.compose_cycle_message(
        tmp_path, SINCE, "failure", "tests=success scan=failure")
    assert "KALSHI_CURRENT" in title and "STRIKE_INCONSISTENCY" in title
    assert "[KALSHI_CURRENT]" in body and "[STRIKE_INCONSISTENCY]" in body
    assert tags == ["warning"]


def test_strategy_step_failure_is_reported_without_blaming_current(tmp_path):
    current_ok(tmp_path)
    strat(tmp_path, "buy_all_no", ok=0, error="TimeoutError()", near=False)
    title, body, _, _ = notify.compose_cycle_message(
        tmp_path, SINCE, "success", "tests=success scan=success strategies=failure")
    assert "KALSHI_CURRENT" not in title
    assert "BUY_ALL_NO" in body and "TimeoutError" in body


def test_daily_summary_has_all_four_strategies(tmp_path):
    current_ok(tmp_path)
    strat(tmp_path, "buy_all_no", executable=True)
    save_json(tmp_path / "rep" / "live_summary.json", {
        "generated_at": NOW, "opportunities": 0, "errors": 0,
        "paper": {"cash": 100.0, "realized_net": 0.0}})
    title, body, _, _ = notify.compose_daily_message(
        tmp_path, tmp_path / "rep", now=datetime(2026, 10, 7, 12, 7, tzinfo=timezone.utc),
        starting_cash=100.0)
    assert title == "Pie a pie: resumen diario"
    for tag in ("[KALSHI_CURRENT]", "[BUY_ALL_NO]", "[STRIKE_INCONSISTENCY]",
                "[FUNDING_BASIS]"):
        assert tag in body
    assert "net+ 1 | ejec. 1" in body
    assert "[STRIKE_INCONSISTENCY]\nsin datos todavía" in body
    assert "Vivo (" in body and "Ciclos 24h: 1 (0 fallidos)" in body
