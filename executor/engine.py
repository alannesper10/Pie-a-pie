"""Motor paper del ejecutor de órdenes de HORUS.

Ciclo: submit (validación, firma, idempotencia, límites) -> step() periódico
(entrada, ejecución con libros re-pedidos tras la latencia, salida por stop,
objetivo o tiempo) -> reportes pieapie.report/v1 en el buzón de salida.

Pie a Pie NO cambia la estrategia: si no puede cumplir la orden dentro de
sus parámetros, la detiene (HALTED_NEEDS_INSTRUCTION o EXPIRED) e informa.
"""

import json
import os
import time
from pathlib import Path

from . import PAPER_ONLY
from .limits import check_order
from .router import best_price, mark_price, route
from .schema import (CANCEL_SCHEMA, ORDER_SCHEMA, REPORT_SCHEMA, check_signature, now_utc, parse_ts,
                     validate_cancel, validate_order)
from .state import (ACCEPTED, CANCELLED, CLOSED, ENTERING, EXITING, EXPIRED, HALTED, INVALIDATED,
                    OPEN, REJECTED, TERMINAL, WAITING_ENTRY)

FEE_STATUS = "ASSUMED"     # comisiones de nivel base público (lab/fees); no verificadas por cuenta


class PaperLedger:
    """Capital del ejecutor (separado de las estrategias del laboratorio)."""

    def __init__(self, store, capital):
        self.store = store
        st = store.get("ledger")
        if st is None:
            st = {"capital": capital, "cash": capital, "inventory": {}, "realized": 0.0}
            store.put("ledger", st)
        self.st = st

    @property
    def cash(self):
        return self.st["cash"]

    def inventory(self, asset):
        return self.st["inventory"].get(asset, {}).get("qty", 0.0)

    def exposure_usd(self):
        return sum(x["cost_usd"] for x in self.st["inventory"].values())

    def buy(self, asset, qty, cost_usd_incl_fees):
        inv = self.st["inventory"].setdefault(asset, {"qty": 0.0, "cost_usd": 0.0})
        inv["qty"] += qty
        inv["cost_usd"] += cost_usd_incl_fees
        self.st["cash"] -= cost_usd_incl_fees
        self.store.put("ledger", self.st)

    def sell(self, asset, qty, proceeds_net):
        """-> costo de lo vendido (costo promedio)."""
        inv = self.st["inventory"][asset]
        basis = inv["cost_usd"] * qty / inv["qty"]
        inv["qty"] -= qty
        inv["cost_usd"] -= basis
        if inv["qty"] <= 1e-12:
            del self.st["inventory"][asset]
        self.st["cash"] += proceeds_net
        self.st["realized"] += proceeds_net - basis
        self.store.put("ledger", self.st)
        return basis


class Engine:
    def __init__(self, store, limits, books_fn, clock=now_utc, latency_s=0.5, sleep=time.sleep,
                 hmac_key=None, outbox=None):
        assert PAPER_ONLY and limits.get("paper_only") is True
        self.store, self.limits, self.books_fn = store, limits, books_fn
        self.clock, self.latency_s, self.sleep = clock, latency_s, sleep
        self.hmac_key = hmac_key if hmac_key is not None else os.environ.get("PIEAPIE_HORUS_HMAC_KEY")
        self.outbox = Path(outbox) if outbox else None
        self.ledger = PaperLedger(store, limits["paper_capital_usd"])
        self.reports = []

    # ------------------------------------------------------------ helpers
    def _meta(self, oid):
        return self.store.get(f"meta:{oid}", {})

    def _set_meta(self, oid, **kw):
        m = self._meta(oid)
        m.update(kw)
        self.store.put(f"meta:{oid}", m)
        return m

    def _books(self, o):
        ins = o["instrument"]
        venues = [v for v in ins["venues_allowed"] if v not in (ins.get("venues_forbidden") or [])]
        books, errs = self.books_fn(ins["symbol"], venues)
        return {v: b for v, b in books.items() if v in venues}, venues, errs

    def _emit(self, oid, ev, mark=None):
        rep = self.report(oid, ev, mark)
        self.reports.append(rep)
        if self.outbox:
            self.outbox.mkdir(parents=True, exist_ok=True)
            (self.outbox / f"{oid}-{ev['seq']:08d}.json").write_text(
                json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
        return rep

    def _go(self, oid, to, reason, detail=None, mark=None):
        ev = self.store.transition(oid, to, reason, detail)
        return self._emit(oid, ev, mark)

    def _reject_unstored(self, payload, reason, detail):
        oid = str(payload.get("order_id", ""))[:64] if isinstance(payload, dict) else ""
        self.store.reject_message(oid, reason, detail, payload)
        rep = {"schema": REPORT_SCHEMA, "order_id": oid, "seq": None, "ts": self.clock().isoformat(),
               "state": REJECTED, "previous_state": None, "reason_code": reason, "detail": detail}
        self.reports.append(rep)
        if self.outbox and oid:
            self.outbox.mkdir(parents=True, exist_ok=True)
            (self.outbox / f"{oid}-rejected-{int(time.time() * 1000)}.json").write_text(
                json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
        return rep

    # ------------------------------------------------------------ entrada
    def submit(self, payload):
        if not isinstance(payload, dict) or payload.get("schema") != ORDER_SCHEMA:
            return self._reject_unstored(payload, "SCHEMA_INVALID", ["schema desconocido"])
        if payload.get("mode") not in (None, "paper"):
            return self._reject_unstored(payload, "REAL_MODE_NOT_AUTHORIZED",
                                         "solo se aceptan órdenes en modo paper")
        errs = validate_order(payload)
        if errs:
            return self._reject_unstored(payload, "SCHEMA_INVALID", errs)
        auth, sig_err = check_signature(payload, self.hmac_key)
        if sig_err:
            return self._reject_unstored(payload, sig_err, "firma HMAC ausente o inválida")
        status, state = self.store.submit(payload, authenticated=auth)
        oid = payload["order_id"]
        if status == "DUPLICATE_SAME":
            return {"schema": REPORT_SCHEMA, "order_id": oid, "state": state,
                    "reason_code": "DUPLICATE_SAME", "detail": "orden ya recibida; sin cambios"}
        if status == "DUPLICATE_CONFLICT":
            return {"schema": REPORT_SCHEMA, "order_id": oid, "state": state,
                    "reason_code": "DUPLICATE_ORDER_ID_CONFLICT",
                    "detail": "mismo order_id con otro contenido: rechazado; la orden original no cambia"}
        now = self.clock()
        if parse_ts(payload["valid_until"]) <= now:
            return self._go(oid, REJECTED, "EXPIRED", {"valid_until": payload["valid_until"]})
        books, venues, berrs = self._books(payload)
        ref = best_price(books, venues, payload["direction"])
        problems = check_order(payload, self.limits, self.ledger, ref)
        open_n = len(self.store.orders(states={ACCEPTED, WAITING_ENTRY, ENTERING, OPEN, EXITING, HALTED}))
        if open_n >= self.limits.get("max_open_orders", 5):
            problems.append(("LIMIT_EXPOSURE", {"open_orders": open_n}))
        if problems:
            return self._go(oid, REJECTED, problems[0][0], {"problems": problems, "ref_price": ref,
                                                            "data_errors": berrs})
        self._set_meta(oid, accepted_ref_price=ref, authenticated=auth)
        self._go(oid, ACCEPTED, "ACCEPTED", {"ref_price": ref, "authenticated": auth,
                                             "limits_applied": {k: self.limits[k] for k in (
                                                 "max_notional_per_order_usd", "max_total_exposure_usd",
                                                 "max_loss_per_order_usd")}})
        return self._go(oid, WAITING_ENTRY, "ACCEPTED", {})

    def cancel(self, msg):
        errs = validate_cancel(msg)
        if errs:
            return self._reject_unstored(msg, "SCHEMA_INVALID", errs)
        auth, sig_err = check_signature(msg, self.hmac_key)
        if sig_err:
            return self._reject_unstored(msg, sig_err, "firma de la cancelación")
        oid = msg["order_id"]
        cur = self.store.order(oid)
        if not cur:
            return self._reject_unstored(msg, "UNKNOWN_ORDER", "no existe la orden")
        st = cur["state"]
        if st in TERMINAL:
            return {"schema": REPORT_SCHEMA, "order_id": oid, "state": st, "reason_code": st,
                    "detail": "la orden ya terminó; cancelación sin efecto"}
        if msg.get("close_position") and st in (OPEN, HALTED) and self._position_qty(oid) > 0:
            self._set_meta(oid, exit_started=self.clock().isoformat(), exit_reason="CANCELLED_BY_HORUS")
            return self._go(oid, EXITING, "CANCELLED_BY_HORUS", {"reason": msg.get("reason"),
                                                                  "close_position": True})
        return self._go(oid, CANCELLED, "CANCELLED_BY_HORUS",
                        {"reason": msg.get("reason"), "position_qty_kept": self._position_qty(oid)})

    def process_message(self, msg):
        schema = msg.get("schema") if isinstance(msg, dict) else None
        if schema == CANCEL_SCHEMA:
            return self.cancel(msg)
        return self.submit(msg)

    # ------------------------------------------------------------ ciclo
    def step(self):
        for o in self.store.orders(states={WAITING_ENTRY, ENTERING, OPEN, EXITING}):
            try:
                getattr(self, f"_step_{o['state'].lower()}")(o["order_id"], o["payload"])
            except Exception as e:  # noqa: BLE001 - un error detiene la orden, no el motor
                if self.store.order(o["order_id"])["state"] not in TERMINAL:
                    self._go(o["order_id"], HALTED, "DATA_UNAVAILABLE",
                             {"error": f"{type(e).__name__}: {str(e)[:200]}"})

    def _step_waiting_entry(self, oid, o):
        now = self.clock()
        if now >= parse_ts(o["valid_until"]):
            return self._go(oid, EXPIRED, "EXPIRED", {"valid_until": o["valid_until"]})
        if o.get("valid_from") and now < parse_ts(o["valid_from"]):
            return None
        books, venues, errs = self._books(o)
        bid, ask = best_price(books, venues, "sell"), best_price(books, venues, "buy")
        if bid is None or ask is None:
            return self.store.note(oid, "DATA_UNAVAILABLE", {"errors": errs})
        mid = (bid + ask) / 2
        for inv in o.get("invalidation") or []:
            t, v = inv["type"], inv["value"]
            if (t == "price_above" and mid > v) or (t == "price_below" and mid < v) or \
                    (t == "time_after" and now > parse_ts(v)):
                return self._go(oid, INVALIDATED, "INVALIDATED", {"condition": inv, "mid": mid})
        en, side = o["entry"], o["direction"]
        contra = ask if side == "buy" else bid
        if en["type"] == "limit":
            ok = contra <= en["limit_price"] if side == "buy" else contra >= en["limit_price"]
        elif en["type"] == "trigger":
            ok = (en.get("trigger_above") is not None and mid >= en["trigger_above"]) or \
                 (en.get("trigger_below") is not None and mid <= en["trigger_below"])
        else:
            ok = True
        if not ok:
            return None
        dev = abs(contra / self._meta(oid).get("accepted_ref_price", contra) - 1) * 1e4
        if en["type"] == "market" and dev > self.limits["max_decision_price_deviation_bps"]:
            return self._go(oid, HALTED, "SLIPPAGE_EXCEEDED",
                            {"deviation_bps": dev, "max": self.limits["max_decision_price_deviation_bps"],
                             "detail": "el precio se movió demasiado desde la aceptación"})
        self._set_meta(oid, decision_price=contra, entry_started=now.isoformat())
        return self._go(oid, ENTERING, "ENTRY_CONDITION_MET", {"decision_price": contra, "mid": mid})

    def _target(self, o, decision_price):
        sz = o["sizing"]
        return ("qty", sz["qty"]) if sz.get("qty") else ("notional", sz["notional_usd"])

    def _filled(self, oid, phase):
        f = self.store.fills(oid, phase)
        return sum(x["qty"] for x in f), sum(x["qty"] * x["price"] for x in f), sum(x["fee_usd"] for x in f)

    def _execute(self, oid, o, phase, side, qty=None, notional=None, ref_price=None):
        """Re-pide libros tras la latencia y ejecuta dentro del deslizamiento máximo."""
        self.sleep(self.latency_s)
        books, venues, errs = self._books(o)
        en = o["entry"]
        lim = ref_price * (1 + en["max_slippage_bps"] / 1e4) if side == "buy" else \
            ref_price * (1 - en["max_slippage_bps"] / 1e4)
        if phase == "entry" and en["type"] == "limit":
            lim = min(lim, en["limit_price"]) if side == "buy" else max(lim, en["limit_price"])
        r = route(books, venues, side, qty=qty, notional=notional, limit_price=lim)
        seq = self.store.next_fill_seq(oid)
        base = o["instrument"]["symbol"].split("/")[0]
        for f in r["fills"]:
            if not self.store.add_fill(oid, seq, phase, f["venue"], side, f["price"], f["qty"],
                                       f["fee_usd"], FEE_STATUS):
                continue
            seq += 1
            if side == "buy":
                self.ledger.buy(base, f["qty"], f["qty"] * f["price"] + f["fee_usd"])
            else:
                self.ledger.sell(base, f["qty"], f["qty"] * f["price"] - f["fee_usd"])
        return r, errs, lim

    def _step_entering(self, oid, o):
        m = self._meta(oid)
        side, dp = o["direction"], m["decision_price"]
        kind, target = self._target(o, dp)
        got, spent, _ = self._filled(oid, "entry")
        rem_q = target - got if kind == "qty" else None
        rem_n = target - spent if kind == "notional" else None
        if (rem_q is not None and rem_q > 1e-12) or (rem_n is not None and rem_n > 1e-6):
            r, errs, lim = self._execute(oid, o, "entry", side, qty=rem_q, notional=rem_n, ref_price=dp)
            if r["fills"]:
                self.store.note(oid, "FILLED", {"fills": r["fills"], "limit_price": lim,
                                                "venues_used": r["venues_used"],
                                                "saving_vs_best_single_usd": r["saving_vs_best_single_usd"]})
        got, spent, _ = self._filled(oid, "entry")
        done = (kind == "qty" and got >= target - 1e-12) or (kind == "notional" and spent >= target - 1e-6)
        if done:
            return self._finish_entry(oid, o, partial=False)
        waited = (self.clock() - parse_ts(m["entry_started"])).total_seconds()
        if waited < o["entry"]["max_wait_s"]:
            return None
        if got <= 1e-12:
            return self._go(oid, EXPIRED, "SLIPPAGE_EXCEEDED",
                            {"detail": "no hubo liquidez dentro del deslizamiento máximo en el plazo",
                             "max_wait_s": o["entry"]["max_wait_s"]})
        if o["entry"].get("allow_partial"):
            return self._finish_entry(oid, o, partial=True)
        return self._go(oid, HALTED, "PARTIAL_TIMEOUT",
                        {"filled_qty": got, "target": target, "kind": kind,
                         "detail": "ejecución parcial no autorizada: se detiene y se pide instrucción"})

    def _finish_entry(self, oid, o, partial):
        reason = "PARTIAL_TIMEOUT" if partial else "FILLED"
        if o["direction"] == "sell":
            return self._go(oid, CLOSED, reason, {"partial": partial})
        return self._go(oid, OPEN, reason, {"partial": partial})

    def _position_qty(self, oid):
        q_in = sum(f["qty"] for f in self.store.fills(oid, "entry") if f["side"] == "buy")
        q_out = sum(f["qty"] for f in self.store.fills(oid, "exit"))
        return max(0.0, q_in - q_out)

    def _step_open(self, oid, o):
        ex = o.get("exit") or {}
        if not ex:
            return None                       # sin salida definida: la posición queda a la espera de HORUS
        books, venues, errs = self._books(o)
        mark = mark_price(books, venues)
        now = self.clock()
        reason = None
        if mark is not None and ex.get("stop") and mark <= ex["stop"]:
            reason = "STOP_HIT"
        elif mark is not None and ex.get("take_profit") and mark >= ex["take_profit"]:
            reason = "TAKE_PROFIT_HIT"
        elif ex.get("time_exit_at") and now >= parse_ts(ex["time_exit_at"]):
            reason = "TIME_EXIT"
        if mark is None:
            return self.store.note(oid, "DATA_UNAVAILABLE", {"errors": errs})
        if reason:
            self._set_meta(oid, exit_started=now.isoformat(), exit_reason=reason, exit_ref=mark)
            return self._go(oid, EXITING, reason, {"mark": mark}, mark=mark)
        return None

    def _step_exiting(self, oid, o):
        m = self._meta(oid)
        qty = self._position_qty(oid)
        if qty > 1e-12:
            ref = m.get("exit_ref")
            if ref is None:
                books, venues, _ = self._books(o)
                ref = mark_price(books, venues)
                self._set_meta(oid, exit_ref=ref)
            if ref is not None:
                r, errs, lim = self._execute(oid, o, "exit", "sell", qty=qty, ref_price=ref)
                if r["fills"]:
                    self.store.note(oid, "FILLED", {"phase": "exit", "fills": r["fills"], "limit_price": lim})
        if self._position_qty(oid) <= 1e-12:
            return self._go(oid, CLOSED, m.get("exit_reason", "FILLED"), {})
        waited = (self.clock() - parse_ts(m["exit_started"])).total_seconds()
        if waited >= o["entry"]["max_wait_s"]:
            return self._go(oid, HALTED, "SLIPPAGE_EXCEEDED",
                            {"remaining_qty": self._position_qty(oid),
                             "detail": "no se pudo salir dentro del deslizamiento: se pide instrucción"})
        return None

    # ------------------------------------------------------------ reportes
    def report(self, oid, ev=None, mark=None):
        cur = self.store.order(oid)
        o, m = cur["payload"], self._meta(oid)
        fe, fx = self.store.fills(oid, "entry"), self.store.fills(oid, "exit")
        q_in = sum(f["qty"] for f in fe)
        cost_in = sum(f["qty"] * f["price"] for f in fe)
        fees = sum(f["fee_usd"] for f in fe + fx)
        avg_in = cost_in / q_in if q_in else None
        dp = m.get("decision_price")
        slip = None
        if avg_in and dp:
            slip = ((avg_in / dp - 1) if o["direction"] == "buy" else (dp / avg_in - 1)) * 1e4
        realized = unrealized = None
        pos = self._position_qty(oid) if o["direction"] == "buy" else 0.0
        if o["direction"] == "buy" and fx:
            q_out = sum(f["qty"] for f in fx)
            proceeds = sum(f["qty"] * f["price"] - f["fee_usd"] for f in fx)
            basis = (cost_in + sum(f["fee_usd"] for f in fe)) * (q_out / q_in) if q_in else 0
            realized = proceeds - basis
        if pos > 0 and mark is not None and q_in:
            unit = (cost_in + sum(f["fee_usd"] for f in fe)) / q_in
            unrealized = pos * (mark - unit)
        return {"schema": REPORT_SCHEMA, "order_id": oid, "seq": (ev or {}).get("seq"),
                "ts": (ev or {}).get("ts"), "state": cur["state"],
                "previous_state": (ev or {}).get("from_state"), "reason_code": (ev or {}).get("reason"),
                "detail": (ev or {}).get("detail"), "strategy": o["strategy"],
                "authenticated": cur["authenticated"], "decision_price": dp,
                "fills": fe + fx, "filled_qty": q_in, "avg_price": avg_in, "slippage_bps": slip,
                "costs": {"verified_usd": 0.0, "assumed_usd": fees, "fee_status": FEE_STATUS},
                "position_qty": pos, "capital_locked_usd": (cost_in * pos / q_in) if q_in else 0.0,
                "realized_pnl_usd": realized, "unrealized_pnl_usd": unrealized,
                "data_sources": o["instrument"]["venues_allowed"], "mode": "paper"}
