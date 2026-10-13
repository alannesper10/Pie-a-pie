"""Registro económico común: teórico y realizado nunca se mezclan."""

import json

import pytest

from lab.record import EconomicRecord, from_kalshi_position, from_lab_row, summarize


def base(**kw):
    d = dict(source="lab", strategy="s", key="k", ts="2026-10-13T00:00:00+00:00",
             nature="arbitrage", evidence="SIMULATED")
    d.update(kw)
    return EconomicRecord(**d)


def test_realized_without_close_evidence_is_invalid():
    assert base(realized_pnl_usd=1.0).validate()
    assert base(evidence="REALIZED_PAPER").validate()
    assert base(evidence="REALIZED_PAPER", realized_pnl_usd=0.5).validate() == []


def test_locked_cannot_exceed_committed_and_fill_ratio_bounds():
    assert base(capital_committed_usd=10, capital_locked_usd=11).validate()
    assert base(fill_ratio=1.2).validate()


def test_lab_rows_are_never_realized():
    row = {"strategy": "cash_and_carry", "key": "binance|ETH", "ts": "t", "stage": "SIMULATED",
           "classification": "ARBITRAJE_GARANTIZADO", "reason": "FILLED", "venues": ["binance"],
           "instruments": ["ETH/USDT", "ETH/USDT:USDT-261225"], "capital_usd": 90.39,
           "gross_usd": 0.39, "costs_verified_usd": 0.0, "costs_assumed_usd": 0.158,
           "net_estimated_usd": 0.232, "size": 0.018, "lock_hours": 1741.6,
           "sim": {"status": "FILLED", "net_usd": 0.238, "matched": 0.018}}
    r = from_lab_row(row)
    assert r.validate() == [] and r.realized_pnl_usd is None
    assert r.expected_net_usd == pytest.approx(0.238) and r.capital_locked_usd == pytest.approx(90.39)
    assert r.fill_ratio == pytest.approx(1.0) and r.expected_net_pct == pytest.approx(0.238 / 90.39)
    obs = from_lab_row({**row, "stage": "OBSERVED", "sim": None})
    assert obs.expected_net_usd is None and obs.capital_locked_usd == 0


def test_kalshi_open_positions_from_real_state_are_unrealized_and_read_only():
    with open("data/state.json", encoding="utf-8") as f:
        before = f.read()
    paper = json.loads(before)["paper"]
    recs = [from_kalshi_position(p, "now", category="ESPECULATIVA") for p in paper["open"]]
    assert {r.key for r in recs} >= {"KXCRITICSPROD-27", "KXCRITICSCOM-27"}
    assert all(r.realized_pnl_usd is None and r.validate() == [] for r in recs)
    prod = next(r for r in recs if r.key == "KXCRITICSPROD-27")
    assert prod.capital_committed_usd == pytest.approx(9.84)
    with open("data/state.json", encoding="utf-8") as f:
        assert f.read() == before                      # solo lectura


def test_closed_kalshi_position_realizes_payout_minus_outlay():
    r = from_kalshi_position({"event_ticker": "E", "cost": 9.0, "fees": 0.5, "slippage": 0.1,
                              "payout": 10.0, "expected_net": 0.4}, "now")
    assert r.evidence == "REALIZED_PAPER" and r.realized_pnl_usd == pytest.approx(0.4)
    assert r.capital_locked_usd == 0


def test_summary_keeps_expected_and_realized_apart():
    s = summarize([base(expected_net_usd=1.0, capital_committed_usd=5, capital_locked_usd=5),
                   base(evidence="REALIZED_PAPER", realized_pnl_usd=-0.2, capital_committed_usd=5)])
    assert s["s"]["realized_pnl_usd"] == pytest.approx(-0.2)
    assert s["s"]["expected_net_usd_open"] == pytest.approx(1.0)
