"""Persistencia del ejecutor: órdenes (idempotentes), eventos inmutables
encadenados por hash, ejecuciones sin duplicados y ledger paper.

lab_data/executor.sqlite, fuera de git. Los eventos solo se agregan; cada
uno guarda el hash del anterior, así que una alteración del historial se
detecta con verify_chain()."""

import hashlib
import json
import sqlite3
from pathlib import Path

from .schema import now_utc, payload_hash
from .state import RECEIVED, TransitionError, can_transition

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY, payload TEXT, payload_hash TEXT,
    state TEXT, authenticated INTEGER, created TEXT, updated TEXT);
CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT, ts TEXT,
    from_state TEXT, to_state TEXT, reason TEXT, detail TEXT, prev_hash TEXT, hash TEXT);
CREATE TABLE IF NOT EXISTS fills (order_id TEXT, fill_seq INTEGER, phase TEXT, venue TEXT,
    side TEXT, price REAL, qty REAL, fee_usd REAL, fee_status TEXT, ts TEXT,
    PRIMARY KEY (order_id, fill_seq));
CREATE TABLE IF NOT EXISTS rejected_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT,
    order_id TEXT, reason TEXT, detail TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS ledger (k TEXT PRIMARY KEY, v TEXT);
"""
GENESIS = "0" * 64


def _ts():
    return now_utc().isoformat(timespec="milliseconds")


class ExecutorStore:
    def __init__(self, path=Path("lab_data") / "executor.sqlite"):
        self.path = Path(path)
        if str(path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path))
        self.db.executescript(SCHEMA)

    # ------------------------------------------------------------- órdenes
    def submit(self, payload: dict, authenticated: bool):
        """Idempotente. -> ("NEW" | "DUPLICATE_SAME" | "DUPLICATE_CONFLICT", estado)."""
        oid, h = payload["order_id"], payload_hash(payload)
        row = self.db.execute("SELECT payload_hash, state FROM orders WHERE order_id=?", (oid,)).fetchone()
        if row:
            if row[0] == h:
                return "DUPLICATE_SAME", row[1]
            self.reject_message(oid, "DUPLICATE_ORDER_ID_CONFLICT",
                                "mismo order_id con contenido distinto; se conserva la orden original",
                                payload)
            return "DUPLICATE_CONFLICT", row[1]
        t = _ts()
        self.db.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?)",
                        (oid, json.dumps(payload, sort_keys=True), h, RECEIVED, int(authenticated), t, t))
        self._event(oid, None, RECEIVED, "RECEIVED", {"payload_hash": h, "authenticated": authenticated})
        self.db.commit()
        return "NEW", RECEIVED

    def order(self, oid):
        r = self.db.execute("SELECT payload, state, authenticated FROM orders WHERE order_id=?",
                            (oid,)).fetchone()
        return None if not r else {"payload": json.loads(r[0]), "state": r[1], "authenticated": bool(r[2])}

    def orders(self, states=None):
        q = "SELECT order_id FROM orders"
        rows = self.db.execute(q + " ORDER BY created").fetchall()
        out = [self.order(r[0]) | {"order_id": r[0]} for r in rows]
        return [o for o in out if states is None or o["state"] in states]

    def transition(self, oid, to_state, reason, detail=None):
        cur = self.order(oid)
        if cur is None:
            raise TransitionError(f"orden desconocida {oid}")
        if not can_transition(cur["state"], to_state):
            raise TransitionError(f"{oid}: {cur['state']} -> {to_state} no permitida")
        self.db.execute("UPDATE orders SET state=?, updated=? WHERE order_id=?", (to_state, _ts(), oid))
        ev = self._event(oid, cur["state"], to_state, reason, detail or {})
        self.db.commit()
        return ev

    def note(self, oid, reason, detail=None):
        """Evento informativo sin cambio de estado (p. ej. ejecución parcial)."""
        st = self.order(oid)["state"]
        ev = self._event(oid, st, st, reason, detail or {})
        self.db.commit()
        return ev

    # ------------------------------------------------------------- eventos
    def _event(self, oid, frm, to, reason, detail):
        prev = self.db.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
        prev = prev[0] if prev else GENESIS
        ts = _ts()
        body = json.dumps([oid, ts, frm, to, reason, detail, prev], sort_keys=True, default=str)
        h = hashlib.sha256(body.encode()).hexdigest()
        cur = self.db.execute("INSERT INTO events (order_id, ts, from_state, to_state, reason, detail,"
                              " prev_hash, hash) VALUES (?,?,?,?,?,?,?,?)",
                              (oid, ts, frm, to, reason, json.dumps(detail, sort_keys=True, default=str),
                               prev, h))
        return {"seq": cur.lastrowid, "order_id": oid, "ts": ts, "from_state": frm, "to_state": to,
                "reason": reason, "detail": detail}

    def events(self, oid=None):
        q = "SELECT seq, order_id, ts, from_state, to_state, reason, detail FROM events"
        rows = self.db.execute(q + (" WHERE order_id=?" if oid else "") + " ORDER BY seq",
                               (oid,) if oid else ()).fetchall()
        return [{"seq": r[0], "order_id": r[1], "ts": r[2], "from_state": r[3], "to_state": r[4],
                 "reason": r[5], "detail": json.loads(r[6])} for r in rows]

    def verify_chain(self):
        """True si ningún evento fue alterado, borrado ni reordenado."""
        prev = GENESIS
        for oid, ts, frm, to, reason, detail, p, h in self.db.execute(
                "SELECT order_id, ts, from_state, to_state, reason, detail, prev_hash, hash "
                "FROM events ORDER BY seq"):
            body = json.dumps([oid, ts, frm, to, reason, json.loads(detail), prev], sort_keys=True,
                              default=str)
            if p != prev or hashlib.sha256(body.encode()).hexdigest() != h:
                return False
            prev = h
        return True

    # ------------------------------------------------------------- fills
    def add_fill(self, oid, fill_seq, phase, venue, side, price, qty, fee_usd, fee_status):
        """Idempotente por (order_id, fill_seq): un reproceso no duplica."""
        cur = self.db.execute("INSERT OR IGNORE INTO fills VALUES (?,?,?,?,?,?,?,?,?,?)",
                              (oid, fill_seq, phase, venue, side, price, qty, fee_usd, fee_status, _ts()))
        self.db.commit()
        return cur.rowcount == 1

    def fills(self, oid, phase=None):
        q = "SELECT fill_seq, phase, venue, side, price, qty, fee_usd, fee_status, ts FROM fills WHERE order_id=?"
        args = [oid]
        if phase:
            q += " AND phase=?"
            args.append(phase)
        return [dict(zip(("fill_seq", "phase", "venue", "side", "price", "qty", "fee_usd", "fee_status", "ts"), r))
                for r in self.db.execute(q + " ORDER BY fill_seq", args)]

    def next_fill_seq(self, oid):
        r = self.db.execute("SELECT MAX(fill_seq) FROM fills WHERE order_id=?", (oid,)).fetchone()
        return 0 if r[0] is None else r[0] + 1

    # ------------------------------------------------------------- otros
    def reject_message(self, oid, reason, detail, payload):
        self.db.execute("INSERT INTO rejected_messages (ts, order_id, reason, detail, payload) VALUES (?,?,?,?,?)",
                        (_ts(), oid, reason, json.dumps(detail, default=str), json.dumps(payload, default=str)))
        self.db.commit()

    def rejected_messages(self):
        return [dict(zip(("ts", "order_id", "reason", "detail"), r)) for r in self.db.execute(
            "SELECT ts, order_id, reason, detail FROM rejected_messages ORDER BY id")]

    def get(self, k, default=None):
        r = self.db.execute("SELECT v FROM ledger WHERE k=?", (k,)).fetchone()
        return json.loads(r[0]) if r else default

    def put(self, k, v):
        self.db.execute("INSERT OR REPLACE INTO ledger VALUES (?,?)", (k, json.dumps(v)))
        self.db.commit()
