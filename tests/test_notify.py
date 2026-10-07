from datetime import datetime, timezone

import pytest
import requests

from src import notify
from src.paper_trader import PaperBook
from src.tracking import (
    CYCLE_FIELDS, NEAR_MISS_FIELDS, PAPER_FIELDS, append_csv, save_json,
)

OLD = "2026-10-07T10:00:00+00:00"
NOW = "2026-10-07T12:00:00+00:00"
SINCE = datetime.fromisoformat("2026-10-07T11:59:00+00:00")
TOPIC = "topic-secreto-123"


def cycle(d, ts=NOW, ok=1, error=""):
    append_csv(d / "cycles.csv", CYCLE_FIELDS,
               {"timestamp": ts, "ok": ok, "error": error})


def near(d, ticker="EV", ts=NOW, executable=False):
    append_csv(d / "near_misses.csv", NEAR_MISS_FIELDS, {
        "timestamp": ts, "event_ticker": ticker, "ask_sum": 0.95, "n_legs": 3,
        "est_net": 0.42, "executable": executable,
        "reason": "NET_EDGE_OK" if executable else "NO_POSITIVE_MARGINAL_EDGE"})


def trade(d, action, ts=NOW):
    append_csv(d / "paper_trades.csv", PAPER_FIELDS, {
        "timestamp": ts, "action": action, "event_ticker": "EV",
        "contracts": 10, "expected_net": 0.42, "realized_net": 0.40,
        "cash_after": 99.6})


@pytest.fixture
def no_network(monkeypatch):
    calls = []
    monkeypatch.setattr(notify.requests, "post",
                        lambda *a, **kw: calls.append((a, kw)) or _Ok())
    return calls


class _Ok:
    def raise_for_status(self):
        pass


# --- qué dispara una notificación de ciclo ---

def test_near_misses_alone_do_not_notify(tmp_path):
    cycle(tmp_path)
    near(tmp_path)
    assert notify.build_cycle_message(tmp_path, SINCE) is None


def test_executable_notifies(tmp_path):
    cycle(tmp_path)
    near(tmp_path, "KXGAME-1", executable=True)
    title, body, priority, _ = notify.build_cycle_message(tmp_path, SINCE)
    assert title == "Pie a pie: oportunidad"
    assert "Ejecutable: KXGAME-1" in body and "US$+0.42" in body
    assert priority == 4


def test_paper_open_and_settle_notify(tmp_path):
    cycle(tmp_path)
    trade(tmp_path, "OPEN")
    trade(tmp_path, "SETTLE")
    title, body, _, _ = notify.build_cycle_message(tmp_path, SINCE)
    assert "Paper abierta: EV, 10 contratos" in body
    assert "Paper cerrada: EV, neto US$+0.40" in body
    assert "Caja: US$99.60" in body


def test_rows_from_previous_runs_are_ignored(tmp_path):
    cycle(tmp_path, ts=OLD)
    near(tmp_path, ts=OLD, executable=True)
    trade(tmp_path, "OPEN", ts=OLD)
    cycle(tmp_path)
    assert notify.build_cycle_message(tmp_path, SINCE) is None


def test_failed_cycle_notifies_with_error(tmp_path):
    cycle(tmp_path, ok=0, error="ConnectionError('red caída')")
    title, body, _, _ = notify.build_cycle_message(
        tmp_path, SINCE, "failure", "tests=success scan=failure commit=success")
    assert title == "Pie a pie: falló el ciclo"
    assert "Paso: scan" in body and "ConnectionError" in body


def test_failure_without_cycle_row_still_notifies(tmp_path):
    # Fallaron los tests: el scanner no llegó a escribir nada.
    title, body, _, _ = notify.build_cycle_message(
        tmp_path, SINCE, "failure", "tests=failure scan=skipped commit=success")
    assert title == "Pie a pie: falló el ciclo"
    assert body == "Paso: tests"


# --- resumen diario ---

def test_daily_summary(tmp_path):
    cycle(tmp_path, ts="2026-10-06T08:00:00+00:00")       # > 24 h: no cuenta
    cycle(tmp_path)
    cycle(tmp_path, ok=0)
    near(tmp_path, "A")
    near(tmp_path, "A")
    near(tmp_path, "B", executable=True)
    book = PaperBook(cash=95.5)
    save_json(tmp_path / "state.json", {"paper": book.to_dict(), "streaks": {}})

    title, body, _, _ = notify.build_daily_message(
        tmp_path, now=datetime(2026, 10, 7, 12, 7, tzinfo=timezone.utc),
        starting_cash=100.0)
    assert title == "Pie a pie: resumen diario"
    assert body.splitlines() == [
        "Ciclos 24h: 2 (1 fallidos)",
        "Casi-aciertos: 3 (2 eventos)",
        "Ejecutables: 1",
        "Caja: US$95.50 (bloqueado US$0.00)",
        "Neto realizado: US$+0.00",
    ]


def test_daily_summary_without_data(tmp_path):
    _, body, _, _ = notify.build_daily_message(tmp_path, starting_cash=100.0)
    assert "Ciclos 24h: 0" in body and "Caja: US$100.00" in body


# --- envío ---

def test_missing_topic_skips_without_failing(tmp_path, monkeypatch, no_network,
                                             capsys):
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    monkeypatch.setenv("JOB_STATUS", "failure")
    assert notify.main(["cycle", "--since", NOW, "--data", str(tmp_path)]) == 0
    assert no_network == []
    assert "NTFY_TOPIC no definido" in capsys.readouterr().out


def test_send_uses_json_and_topic_from_env(tmp_path, monkeypatch, no_network,
                                           capsys):
    monkeypatch.setenv("NTFY_TOPIC", TOPIC)
    assert notify.main(["test", "--data", str(tmp_path)]) == 0
    (args, kw), = no_network
    assert args == ("https://ntfy.sh",)
    assert kw["json"]["topic"] == TOPIC
    assert kw["json"]["title"] == "Pie a pie: prueba"
    assert TOPIC not in capsys.readouterr().out          # nunca se imprime


def test_send_error_does_not_raise_or_leak_topic(monkeypatch, capsys):
    def boom(*a, **kw):
        raise requests.ConnectionError(f"https://ntfy.sh/{TOPIC} caído")
    monkeypatch.setattr(notify.requests, "post", boom)
    assert notify.send(TOPIC, "t", "b") is False
    out = capsys.readouterr().out
    assert "No se pudo notificar (ConnectionError)" in out
    assert TOPIC not in out


def test_nothing_to_notify_sends_nothing(tmp_path, monkeypatch, no_network):
    monkeypatch.setenv("NTFY_TOPIC", TOPIC)
    monkeypatch.setenv("JOB_STATUS", "success")
    cycle(tmp_path)
    near(tmp_path)
    assert notify.main(["cycle", "--since", NOW, "--data", str(tmp_path)]) == 0
    assert no_network == []
