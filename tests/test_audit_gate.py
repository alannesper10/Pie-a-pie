import csv
import json

import pytest

import scanner
from src.config import BotConfig
from src.event_arbitrage import evaluate_event_bundle, prefilter_event
from src.guarantee import GUARANTEED, NOT_EXECUTABLE, SPECULATIVE, UNVERIFIABLE


def ob(yes_ask, size):
    """Libro Kalshi con un YES ask (= NO bid de 1 - ask) y un YES bid 0.01 abajo."""
    return {"orderbook_fp": {"no_dollars": [[f"{1 - yes_ask:.4f}", str(size)]],
                             "yes_dollars": [[f"{yes_ask - 0.01:.4f}", str(size)]]}}


class FakeClient:
    """Devuelve libros por ticker; 'after' simula el libro tras la latencia."""

    def __init__(self, before, after=None):
        self.before, self.after, self.calls = before, after or before, {}

    def get_orderbook(self, ticker, timeout=None):
        n = self.calls[ticker] = self.calls.get(ticker, 0) + 1
        return (self.before if n == 1 else self.after)[ticker]


def game_event(asks, title="PSG vs Le Mans"):
    names = ["PSG", "Le Mans", "Tie"]
    ms = []
    for t, n, a in zip("ABT", names, asks):
        rule = (f"If the {title} game ends in a tie, Yes." if n == "Tie"
                else f"If {n} wins the {title} game, Yes.")
        ms.append({"ticker": t, "market_type": "binary", "status": "active", "result": "",
                   "yes_ask_dollars": str(a), "yes_ask_size_fp": "100", "volume_24h_fp": "500",
                   "yes_sub_title": n, "rules_primary": rule})
    return {"event_ticker": "EV", "title": title, "mutually_exclusive": True, "markets": ms}


def run_gate(tmp_path, monkeypatch, before, after=None, title="PSG vs Le Mans", asks=(0.30,) * 3):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("src.execution_check.time.sleep", lambda s: None)
    ev = game_event(asks, title)
    pre, why = prefilter_event(ev, max_prelim_sum=10)
    if pre is None:          # cobertura no probada: no llega a evaluarse
        return None, why
    client = FakeClient(before, after)
    ladders, t0 = scanner.fetch_ladders(client, pre, 10, 10)
    o = evaluate_event_bundle(pre, ladders, fee_coefficient=0.07, slippage_per_contract=0.001,
                              budget_usd=10, min_sane_ask_sum=1 / 1.1)
    assert o.executable
    return scanner.audit_and_gate(client, pre, o, t0, BotConfig(), "2026-10-13T12:00:00+00:00"), None


def audit_rows(tmp_path):
    with open(tmp_path / "data" / "opportunity_audit.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


BOOKS = {"A": ob(0.30, 50), "B": ob(0.30, 50), "T": ob(0.31, 50)}


def test_stable_books_proven_coverage_is_guaranteed(tmp_path, monkeypatch):
    o, _ = run_gate(tmp_path, monkeypatch, BOOKS)
    (row,) = audit_rows(tmp_path)
    assert row["classification"] == GUARANTEED and o.executable
    assert float(row["net_min"]) > 0 and float(row["net_min_stressed"]) > 0
    assert row["coverage_method"] == "HEAD_TO_HEAD_WITH_TIE"
    ev = json.loads((tmp_path / row["evidence"]).read_text())
    assert set(ev["t0_books"]) == set(ev["t1_books"]) == {"A", "B", "T"}
    assert ev["t1_books"]["A"]["fetched_at"] and ev["scenarios"]["undetermined"] == []


def test_price_moves_after_latency_is_not_executable(tmp_path, monkeypatch):
    after = {**BOOKS, "B": ob(0.40, 50)}             # una pata se encareció
    o, _ = run_gate(tmp_path, monkeypatch, BOOKS, after)
    (row,) = audit_rows(tmp_path)
    assert row["exec_status"] == "EJECUCION_FALLIDA"
    assert row["classification"] == NOT_EXECUTABLE and not o.executable


def test_insufficient_depth_after_latency(tmp_path, monkeypatch):
    after = {**BOOKS, "T": ob(0.31, 2)}              # quedan 2 contratos
    o, _ = run_gate(tmp_path, monkeypatch, BOOKS, after)
    (row,) = audit_rows(tmp_path)
    assert "profundidad insuficiente" in row["exec_reason"] and not o.executable


def test_open_list_event_never_reaches_execution(tmp_path, monkeypatch):
    o, why = run_gate(tmp_path, monkeypatch, BOOKS, title="Critics Choice: Best Comedy")
    assert o is None and why == "EXHAUSTIVENESS_UNCONFIRMED"


def test_speculative_open_list_is_logged_with_max_loss(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ev = game_event((0.30, 0.30, 0.30), title="Critics Choice: Best Comedy")
    scanner.log_speculative(ev)
    (row,) = audit_rows(tmp_path)
    assert row["classification"] == SPECULATIVE
    assert float(row["max_loss"]) == pytest.approx(0.90)
    assert float(row["net_expected"]) == pytest.approx(0.10)


def test_only_guaranteed_opens_paper(tmp_path, monkeypatch):
    from src.paper_trader import PaperBook
    o_bad, _ = run_gate(tmp_path, monkeypatch, BOOKS, {**BOOKS, "B": ob(0.40, 50)})
    book = PaperBook(cash=100.0)
    assert book.try_open(o_bad, None, "t")[1] == "NOT_EXECUTABLE"
    (tmp_path / "x").mkdir()
    o_ok, _ = run_gate(tmp_path / "x", monkeypatch, BOOKS)
    pos, why = book.try_open(o_ok, None, "t")
    assert why == "OPENED"
    assert pos.expected_net == pytest.approx(o_ok.net_profit)
