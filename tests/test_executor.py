"""Ejecutor de órdenes de HORUS: contrato v1, idempotencia, auditoría,
límites propios, ruteo y ciclo completo en paper (integración)."""

import copy
import json
from datetime import datetime, timedelta, timezone

import pytest

from executor.engine import Engine
from executor.limits import load_limits
from executor.router import route
from executor.schema import payload_hash, sign, validate_order
from executor.state import (CANCELLED, CLOSED, ENTERING, EXITING, EXPIRED, HALTED, INVALIDATED,
                            OPEN, REJECTED, TransitionError, WAITING_ENTRY, can_transition)
from executor.store import ExecutorStore

T0 = datetime(2026, 10, 14, 15, 0, tzinfo=timezone.utc)


class Clock:
    def __init__(self):
        self.t = T0

    def __call__(self):
        return self.t

    def advance(self, s):
        self.t += timedelta(seconds=s)


class Books:
    """Libros por venue; se pueden cambiar entre pasos."""

    def __init__(self, **venues):
        self.v = venues
        self.calls = 0

    def __call__(self, symbol, venues):
        self.calls += 1
        return {k: copy.deepcopy(b) for k, b in self.v.items() if k in venues}, []


def book(bid, ask, qty=10.0):
    return {"bids": [[bid, qty], [bid - 1, qty]], "asks": [[ask, qty], [ask + 1, qty]]}


def order(**kw):
    o = {"schema": "horus.order/v1", "order_id": "ord-0001", "issuer": "horus",
         "issued_at": T0.isoformat(), "valid_until": (T0 + timedelta(hours=1)).isoformat(),
         "mode": "paper", "strategy": {"name": "trend_breakout", "version": "1.0.0"},
         "instrument": {"asset_class": "crypto_spot", "symbol": "ETH/USDT",
                        "venues_allowed": ["binance", "bybit"]},
         "direction": "buy", "sizing": {"notional_usd": 20.0},
         "entry": {"type": "market", "max_slippage_bps": 20, "max_wait_s": 120, "allow_partial": False},
         "exit": {"take_profit": 105.0, "stop": 98.0},
         "risk": {"max_loss_usd": 5.0}, "on_problem": "halt_and_report"}
    for k, v in kw.items():
        o[k] = v
    return o


@pytest.fixture
def env():
    clock = Clock()
    books = Books(binance=book(99.9, 100.0), bybit=book(99.8, 100.1))
    store = ExecutorStore(":memory:")
    eng = Engine(store, load_limits(), books, clock=clock, latency_s=0, sleep=lambda s: None, hmac_key="")
    return eng, store, books, clock


# ------------------------------------------------------------ contrato

def test_valid_order_passes_and_bad_fields_are_listed():
    assert validate_order(order()) == []
    bad = order(direction="short", sizing={"notional_usd": 10, "qty": 1}, on_problem="improvise")
    errs = validate_order(bad)
    assert any("direction" in e for e in errs) and any("sizing" in e for e in errs)
    assert any("on_problem" in e for e in errs)
    assert any("stop" in e for e in validate_order(order(exit={"take_profit": 90, "stop": 95})))


def test_payload_hash_ignores_signature_and_key_order():
    a = order()
    b = json.loads(json.dumps(a))
    b["signature"] = "x"
    assert payload_hash(a) == payload_hash(dict(reversed(list(b.items()))))


def test_state_machine_rejects_unlisted_transitions():
    assert can_transition(WAITING_ENTRY, ENTERING) and not can_transition(CLOSED, OPEN)
    store = ExecutorStore(":memory:")
    store.submit(order(), authenticated=False)
    with pytest.raises(TransitionError):
        store.transition("ord-0001", OPEN, "x")


# ------------------------------------------------------------ store

def test_idempotency_same_payload_noop_and_conflict_rejected():
    store = ExecutorStore(":memory:")
    assert store.submit(order(), False)[0] == "NEW"
    assert store.submit(order(), False)[0] == "DUPLICATE_SAME"
    assert store.submit(order(sizing={"notional_usd": 30.0}), False)[0] == "DUPLICATE_CONFLICT"
    assert store.order("ord-0001")["payload"]["sizing"] == {"notional_usd": 20.0}
    assert store.rejected_messages()[0]["reason"] == "DUPLICATE_ORDER_ID_CONFLICT"
    assert len(store.events("ord-0001")) == 1


def test_fills_are_idempotent_and_event_chain_detects_tampering():
    store = ExecutorStore(":memory:")
    store.submit(order(), False)
    assert store.add_fill("ord-0001", 0, "entry", "binance", "buy", 100, 0.1, 0.01, "ASSUMED")
    assert not store.add_fill("ord-0001", 0, "entry", "binance", "buy", 100, 0.1, 0.01, "ASSUMED")
    store.transition("ord-0001", REJECTED, "LIMIT_NOTIONAL")
    assert store.verify_chain()
    store.db.execute("UPDATE events SET reason='ACCEPTED' WHERE to_state='REJECTED'")
    assert not store.verify_chain()


# ------------------------------------------------------------ router

def test_router_splits_across_venues_by_effective_price_and_respects_limit():
    books = {"binance": {"asks": [[100.0, 0.1], [100.5, 5]]}, "bybit": {"asks": [[100.2, 5]]}}
    fee = {"binance": 0.001, "bybit": 0.001}.get
    r = route(books, ["binance", "bybit"], "buy", qty=1.0, fee_of=fee)
    assert [f["venue"] for f in r["fills"]] == ["binance", "bybit"]
    assert r["filled_qty"] == pytest.approx(1.0)
    assert r["best_single_venue"] == "bybit" and r["saving_vs_best_single_usd"] >= 0
    capped = route(books, ["binance", "bybit"], "buy", qty=1.0, limit_price=100.1, fee_of=fee)
    assert capped["filled_qty"] == pytest.approx(0.1)


def test_router_fee_can_change_the_best_venue():
    books = {"cheapfee": {"bids": [[99.9, 1]]}, "dear": {"bids": [[100.0, 1]]}}
    r = route(books, ["cheapfee", "dear"], "sell", qty=1.0,
              fee_of={"cheapfee": 0.0005, "dear": 0.012}.get)
    assert r["fills"][0]["venue"] == "cheapfee"


# ------------------------------------------------------------ integración

def test_full_cycle_buy_then_take_profit_reports_realized_separately(env):
    eng, store, books, clock = env
    rep = eng.submit(order())
    assert rep["state"] == WAITING_ENTRY
    eng.step()                                         # condición market -> ENTERING
    assert store.order("ord-0001")["state"] == ENTERING
    eng.step()                                         # ejecuta
    assert store.order("ord-0001")["state"] == OPEN
    r_open = eng.report("ord-0001", mark=99.9)
    assert r_open["realized_pnl_usd"] is None and r_open["unrealized_pnl_usd"] is not None
    books.v["binance"] = book(106.0, 106.1)
    eng.step()
    assert store.order("ord-0001")["state"] == EXITING
    eng.step()
    final = eng.report("ord-0001")
    assert store.order("ord-0001")["state"] == CLOSED
    assert final["realized_pnl_usd"] > 0 and final["unrealized_pnl_usd"] is None
    assert final["position_qty"] == 0 and final["costs"]["fee_status"] == "ASSUMED"
    assert store.verify_chain()
    assert eng.ledger.st["inventory"] == {}


def test_stop_loss_exit(env):
    eng, store, books, clock = env
    eng.submit(order())
    eng.step()
    eng.step()
    books.v = {"binance": book(97.0, 97.1), "bybit": book(96.9, 97.2)}
    eng.step()
    assert store.events("ord-0001")[-1]["reason"] == "STOP_HIT"
    eng.step()
    rep = eng.report("ord-0001")
    assert store.order("ord-0001")["state"] == CLOSED and rep["realized_pnl_usd"] < 0


def test_limits_are_never_exceeded_by_an_order(env):
    eng, store, books, clock = env
    rep = eng.submit(order(order_id="ord-big-01", sizing={"notional_usd": 500.0}))
    assert rep["state"] == REJECTED and rep["reason_code"] == "LIMIT_NOTIONAL"
    rep = eng.submit(order(order_id="ord-nostop1", exit=None, risk={"max_loss_usd": 5.0}))
    assert rep["state"] == REJECTED and rep["reason_code"] == "LIMIT_LOSS"   # sin stop: pérdida = nocional


def test_real_mode_expired_unsigned_and_bad_schema_are_rejected():
    clock = Clock()
    store = ExecutorStore(":memory:")
    books = Books(binance=book(99.9, 100.0))
    eng = Engine(store, load_limits(), books, clock=clock, latency_s=0, sleep=lambda s: None,
                 hmac_key="secreto-de-prueba")
    assert eng.submit(order(mode="real"))["reason_code"] == "REAL_MODE_NOT_AUTHORIZED"
    assert eng.submit(order())["reason_code"] == "SIGNATURE_REQUIRED"
    bad = order(order_id="ord-sig-bad")
    bad["signature"] = "0" * 64
    assert eng.submit(bad)["reason_code"] == "SIGNATURE_INVALID"
    good = order(order_id="ord-sig-good")
    good["signature"] = sign(good, "secreto-de-prueba")
    assert eng.submit(good)["state"] == WAITING_ENTRY
    old = order(order_id="ord-expired", valid_until=(T0 - timedelta(seconds=1)).isoformat(),
                issued_at=(T0 - timedelta(hours=1)).isoformat())
    old["signature"] = sign(old, "secreto-de-prueba")
    assert eng.submit(old)["state"] == REJECTED
    assert eng.submit({"schema": "otra/v9"})["reason_code"] == "SCHEMA_INVALID"


def test_invalidation_and_expiry_before_entry(env):
    eng, store, books, clock = env
    eng.submit(order(order_id="ord-inval1", entry={"type": "limit", "limit_price": 90.0,
                                                    "max_slippage_bps": 20, "max_wait_s": 60},
                     invalidation=[{"type": "price_above", "value": 101.0}]))
    eng.step()
    assert store.order("ord-inval1")["state"] == WAITING_ENTRY      # límite no alcanzado
    books.v["binance"] = book(101.5, 101.6)
    books.v["bybit"] = book(101.5, 101.7)
    eng.step()
    assert store.order("ord-inval1")["state"] == INVALIDATED
    eng.submit(order(order_id="ord-expire1", entry={"type": "limit", "limit_price": 90.0,
                                                     "max_slippage_bps": 20, "max_wait_s": 60}))
    clock.advance(3601)
    eng.step()
    assert store.order("ord-expire1")["state"] == EXPIRED


def test_partial_fill_not_authorized_halts_and_asks_for_instruction(env):
    eng, store, books, clock = env
    thin = {"bids": [[99.9, 1]], "asks": [[100.0, 0.05]]}        # solo US$5 dentro del límite
    books.v = {"binance": thin}
    eng.submit(order(order_id="ord-part01", instrument={"asset_class": "crypto_spot", "symbol": "ETH/USDT",
                                                         "venues_allowed": ["binance"]}))
    eng.step()
    eng.step()
    assert store.order("ord-part01")["state"] == ENTERING        # parcial, sigue esperando
    clock.advance(121)
    eng.step()
    assert store.order("ord-part01")["state"] == HALTED
    assert store.events("ord-part01")[-1]["reason"] == "PARTIAL_TIMEOUT"
    # HORUS decide: cancelar y cerrar lo que se compró
    eng.cancel({"schema": "horus.cancel/v1", "order_id": "ord-part01", "issued_at": T0.isoformat(),
                "reason": "abortar", "close_position": True})
    assert store.order("ord-part01")["state"] == EXITING
    eng.step()
    assert store.order("ord-part01")["state"] == CLOSED


def test_sell_requires_inventory_and_no_double_execution_on_reprocess(env):
    eng, store, books, clock = env
    rep = eng.submit(order(order_id="ord-sell01", direction="sell", exit=None, sizing={"qty": 0.1}))
    assert rep["reason_code"] == "INSUFFICIENT_INVENTORY"
    eng.submit(order())
    eng.step()
    eng.step()
    n = len(store.fills("ord-0001"))
    eng.submit(order())                       # reenvío idéntico: sin efecto
    eng.step()                                # OPEN sin salida alcanzada: no ejecuta de nuevo
    assert len(store.fills("ord-0001")) == n
    assert eng.cancel({"schema": "horus.cancel/v1", "order_id": "ord-0001",
                       "issued_at": T0.isoformat(), "reason": "x"})["state"] == CANCELLED


def test_inbox_processing_moves_files_and_writes_reports(tmp_path, env):
    import run_executor
    eng, store, books, clock = env
    eng.outbox = tmp_path / "outbox"
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    (inbox / "a.json").write_text(json.dumps(order()), encoding="utf-8")
    (inbox / "b.json").write_text("{no es json", encoding="utf-8")
    reps = run_executor.process_inbox(eng, inbox)
    assert [r["state"] for r in reps] == [WAITING_ENTRY, REJECTED]
    assert not list(inbox.glob("*.json")) and len(list((inbox / "processed").glob("*.json"))) == 2
    assert list(eng.outbox.glob("ord-0001-*.json"))
