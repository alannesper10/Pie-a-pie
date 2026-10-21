"""Entradas repetidas válidas en strike_inconsistency (paper)."""

from datetime import datetime, timedelta, timezone

import pytest

from src.notify import _strategy_daily_lines, build_strategy_cycle_lines
from src.paper_trader import PaperBook, PaperPosition
from src.strategies import kalshi_common as kc
from src.strategies.kalshi_common import BundleResult, StrategyStore, open_paper_repeat
from src.tracking import read_csv

KEY = "USCLIMATE-2025|USCLIMATE-2030"


def bundle(contracts=8, avail=20.0, prices=(0.40, 0.568), per=0.968, fees=0.15, slip=0.016):
    cost = per * contracts
    net = contracts * 1.0 - cost - fees - slip
    return BundleResult(
        strategy="strike_inconsistency", event_ticker="USCLIMATE", key=KEY,
        legs=(("USCLIMATE-2025", prices[0], avail), ("USCLIMATE-2030", prices[1], avail)),
        sides=("yes", "no"), min_payout_per_bundle=1.0, contracts=contracts,
        max_contracts_available=avail, pair_cost=per, cost=cost, min_payout=float(contracts),
        gross_profit=contracts - cost, estimated_fees=fees, estimated_slippage=slip, net_profit=net,
        net_profit_per_contract=net / contracts, net_return=net / cost, best_bundle_cost=per,
        executable=True, reason="NET_EDGE_OK")


def store(tmp_path, cash=100.0, open_=None):
    s = StrategyStore(tmp_path, "strike_inconsistency", 100.0, max_gap_min=40)
    s.book = PaperBook(cash=cash, open=list(open_ or []))
    return s


def ts(i):
    return (datetime(2026, 10, 21, 12, tzinfo=timezone.utc) + timedelta(minutes=40 * i)).isoformat(timespec="seconds")


def legs(latest="2026-10-25T12:00:00Z", timer=3600, status="active"):
    return [{"ticker": t, "status": status, "latest_expiration_time": latest,
             "settlement_timer_seconds": timer} for t in ("USCLIMATE-2025", "USCLIMATE-2030")]


def go(s, r, i, limit=25.0, markets=None, approvals=None):
    # por defecto plazo de recupero < 7 días: con neto > 0 es caso A
    return open_paper_repeat(s, r, "2026-10-25T12:00:00Z", ts(i), starting_cash=100.0,
                             max_key_outlay=limit, reference_rate=0.04,
                             markets=legs() if markets is None else markets, approvals=approvals)


def test_successive_valid_entries_reserve_capital_per_entry(tmp_path):
    s = store(tmp_path)
    p1, why1 = go(s, bundle(prices=(0.40, 0.568)), 0)
    p2, why2 = go(s, bundle(prices=(0.39, 0.578)), 1)          # libro nuevo (otro precio): liquidez completa
    assert why1 == "FIRST_ENTRY" and why2 == "NEW_ENTRY"
    assert p1.entry_id != p2.entry_id and p1.key == p2.key == KEY
    assert len(s.book.open_for_key(KEY, "USCLIMATE")) == 2
    assert s.book.cash == pytest.approx(100.0 - p1.outlay - p2.outlay)
    assert s.book.reconcile(100.0) == pytest.approx(0.0)
    entries = read_csv(tmp_path / "strike_inconsistency" / "entries.csv")
    assert [e["entry_id"] for e in entries] == [p1.entry_id, p2.entry_id]
    assert float(entries[1]["key_outlay_after"]) == pytest.approx(p1.outlay + p2.outlay, abs=1e-3)
    trades = read_csv(tmp_path / "strike_inconsistency" / "paper_trades.csv")
    assert [t["action"] for t in trades] == ["OPEN", "OPEN"]           # mismo formato de siempre


def test_insufficient_cash_is_rejected_without_touching_cash(tmp_path):
    s = store(tmp_path, cash=5.0, open_=[PaperPosition("X", ["a"], 1, 95.0, 0, 0, 0, "t", None)])
    pos, why = go(s, bundle(), 0)
    assert pos is None and why == "INSUFFICIENT_CASH" and s.book.cash == 5.0
    d = read_csv(tmp_path / "strike_inconsistency" / "decisions.csv")[-1]
    assert d["decision"] == "REJECTED" and d["reason"] == "INSUFFICIENT_CASH"


def test_technical_retry_of_the_same_cycle_is_not_duplicated(tmp_path):
    s = store(tmp_path)
    p1, _ = go(s, bundle(), 0)
    cash = s.book.cash
    p2, why = go(s, bundle(prices=(0.39, 0.578)), 0)              # mismo ciclo reprocesado
    assert p2 is None and why == "DUPLICATE_ENTRY" and s.book.cash == cash
    assert len(s.book.open) == 1


def test_ledger_mismatch_blocks_new_entries(tmp_path):
    s = store(tmp_path, cash=90.0)                                 # faltan US$10 sin posición que los explique
    pos, why = go(s, bundle(), 0)
    assert pos is None and why == "LEDGER_MISMATCH" and s.book.cash == 90.0


def test_liquidity_already_taken_with_the_same_book(tmp_path):
    s = store(tmp_path)
    p1, _ = go(s, bundle(contracts=8, avail=10.0), 0)
    p2, _ = go(s, bundle(contracts=8, avail=10.0), 1)             # mismo libro: solo quedan 2
    assert p1.contracts == 8 and p2.contracts == 2
    assert p2.expected_net == pytest.approx(p1.expected_net / 8 * 2)  # costos y neto escalados
    p3, why = go(s, bundle(contracts=8, avail=10.0), 2)
    assert p3 is None and why == "LIQUIDITY_ALREADY_TAKEN"


def test_key_limit_and_legacy_position_counts(tmp_path):
    legacy = PaperPosition("USCLIMATE", ["USCLIMATE-2025", "USCLIMATE-2030"], 9, 8.712, 0.17, 0.018,
                           0.10, "2026-10-20T21:31:57+00:00", "2030-12-31T15:00:00Z", sides=["yes", "no"])
    s = store(tmp_path, cash=100.0 - legacy.outlay, open_=[legacy])
    p, why = go(s, bundle(contracts=8, avail=30.0, prices=(0.39, 0.578)), 0, limit=12.0)
    # tope 12: 8,90 ya usados -> caben 3 contratos más (3 × 1,0 = 3,0 ≤ 3,10)
    assert p.contracts == 3
    assert sum(x.outlay for x in s.book.open_for_key(KEY, "USCLIMATE")) <= 12.0 + 1e-9
    _, why2 = go(s, bundle(contracts=8, avail=30.0, prices=(0.38, 0.588)), 1, limit=12.0)
    assert why2 in ("KEY_LIMIT",)
    assert legacy in s.book.open and legacy.entry_id is None      # la posición previa no se altera


def test_reconciliation_after_settlement(tmp_path):
    s = store(tmp_path)
    p1, _ = go(s, bundle(), 0)
    go(s, bundle(prices=(0.39, 0.578)), 1)
    markets = {"USCLIMATE-2025": {"status": "finalized", "result": "yes"},
               "USCLIMATE-2030": {"status": "finalized", "result": "yes"}}
    assert s.book.try_settle(p1, markets, ts(2))
    assert s.book.reconcile(100.0) == pytest.approx(0.0)
    assert s.book.realized_net == pytest.approx(p1.payout - p1.outlay)


def test_default_behavior_of_other_strategies_is_unchanged():
    b = PaperBook(cash=100.0)
    r = bundle()
    p, why = b.try_open(r, None, "t0")
    assert why == "OPENED" and p.entry_id is None
    assert b.try_open(r, None, "t1") == (None, "ALREADY_OPEN")
    d = b.to_dict()["open"][0]
    assert "entry_id" not in d and "key" not in d                   # mismo formato de state.json


def test_state_roundtrip_keeps_entry_fields(tmp_path):
    s = store(tmp_path)
    go(s, bundle(), 0)
    d = s.book.to_dict()
    again = PaperBook.from_dict(d, 100.0)
    assert again.open[0].entry_id == s.book.open[0].entry_id and again.open[0].key == KEY


def test_notifications_distinguish_and_do_not_repeat(tmp_path):
    s = store(tmp_path)
    d = tmp_path / "strike_inconsistency"
    go(s, bundle(contracts=8, avail=10.0), 0)
    lines = build_strategy_cycle_lines(d, datetime.fromisoformat(ts(0)))
    assert any(l.startswith("Nueva entrada efectuada (cumple el mínimo)") and "primera entrada" in l
               for l in lines)
    go(s, bundle(contracts=8, avail=10.0), 1)
    go(s, bundle(contracts=8, avail=10.0), 2)                      # liquidez tomada
    l2 = build_strategy_cycle_lines(d, datetime.fromisoformat(ts(2)))
    assert any("Sin nueva entrada" in l and "liquidez" in l for l in l2)
    go(s, bundle(contracts=8, avail=10.0), 3)                      # mismo rechazo otra vez
    l3 = build_strategy_cycle_lines(d, datetime.fromisoformat(ts(3)))
    assert not any("Sin nueva entrada" in l for l in l3)           # no se repite el aviso
    s.save()                                                       # el resumen lee state.json
    daily = _strategy_daily_lines(d, datetime.fromisoformat(ts(0)) - timedelta(hours=1), 100.0)
    assert "entradas nuevas 2" in daily[1] and "rechazos 1" in daily[1]   # un rechazo que persiste = 1
    assert "P&L realizado US$+0.00" in daily[3] and "(no realizado)" in daily[3]
