"""SQLite del laboratorio (lab_data/, fuera de git). Guarda snapshots crudos
(comprimidos) para replay reproducible, oportunidades, ticks, errores y ledgers."""

import json
import sqlite3
import zlib
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started TEXT, mode TEXT,
    seed INTEGER, source_run TEXT, args TEXT);
CREATE TABLE IF NOT EXISTS snapshots (run_id TEXT, tick INTEGER, ts TEXT, data BLOB,
    PRIMARY KEY (run_id, tick));
CREATE TABLE IF NOT EXISTS opportunities (uid TEXT PRIMARY KEY, run_id TEXT, tick INTEGER,
    ts TEXT, strategy TEXT, key TEXT, stage TEXT, decision TEXT, reason TEXT,
    net_estimated REAL, net_simulated REAL, capital REAL, data TEXT);
CREATE INDEX IF NOT EXISTS opp_run ON opportunities (run_id, strategy);
CREATE TABLE IF NOT EXISTS ticks (run_id TEXT, tick INTEGER, ts TEXT, strategy TEXT,
    seconds REAL, n_opportunities INTEGER, error TEXT);
CREATE TABLE IF NOT EXISTS errors (run_id TEXT, tick INTEGER, data TEXT);
CREATE TABLE IF NOT EXISTS ledgers (run_id TEXT, strategy TEXT, data TEXT,
    PRIMARY KEY (run_id, strategy));
"""


class LabStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.executescript(SCHEMA)

    def start_run(self, run_id, started, mode, seed, source_run=None, args=None):
        self.db.execute("INSERT INTO runs VALUES (?,?,?,?,?,?)",
                        (run_id, started, mode, seed, source_run, json.dumps(args or {})))
        self.db.commit()

    def save_snapshot(self, run_id, snap):
        self.db.execute("INSERT OR REPLACE INTO snapshots VALUES (?,?,?,?)",
                        (run_id, snap.tick, snap.ts, zlib.compress(snap.to_json().encode())))
        self.db.commit()

    def iter_snapshots(self, run_id, start_tick=0):
        """Snapshots de a uno (no carga toda la corrida en memoria)."""
        from .sources import Snapshot
        cur = self.db.execute("SELECT tick FROM snapshots WHERE run_id=? AND tick>=? ORDER BY tick",
                              (run_id, start_tick))
        for (tick,) in cur.fetchall():
            (blob,) = self.db.execute("SELECT data FROM snapshots WHERE run_id=? AND tick=?",
                                      (run_id, tick)).fetchone()
            yield Snapshot.from_json(zlib.decompress(blob).decode())

    def max_tick(self, run_id):
        r = self.db.execute("SELECT MAX(tick) FROM snapshots WHERE run_id=?", (run_id,)).fetchone()
        return -1 if r[0] is None else r[0]

    def load_snapshots(self, run_id):
        from .sources import Snapshot
        rows = self.db.execute("SELECT data FROM snapshots WHERE run_id=? ORDER BY tick",
                               (run_id,)).fetchall()
        return [Snapshot.from_json(zlib.decompress(r[0]).decode()) for r in rows]

    def save_opportunity(self, run_id, o):
        row = o.to_row()
        self.db.execute(
            "INSERT OR REPLACE INTO opportunities VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (o.uid, run_id, o.tick, o.ts, o.strategy, o.key, o.stage, o.decision, o.reason,
             o.net_estimated_usd, o.net_simulated_usd, o.capital_usd,
             json.dumps(row, default=str)))

    def commit(self):
        self.db.commit()

    def log_tick(self, run_id, tick, ts, strategy, seconds, n, error=None):
        self.db.execute("INSERT INTO ticks VALUES (?,?,?,?,?,?,?)",
                        (run_id, tick, ts, strategy, seconds, n, error))

    def log_errors(self, run_id, tick, errors):
        self.db.executemany("INSERT INTO errors VALUES (?,?,?)",
                            [(run_id, tick, json.dumps(e)) for e in errors])

    def save_ledger(self, run_id, strategy, data):
        self.db.execute("INSERT OR REPLACE INTO ledgers VALUES (?,?,?)",
                        (run_id, strategy, json.dumps(data, default=str)))
        self.db.commit()

    def opportunities(self, run_id, strategy=None):
        q = "SELECT data FROM opportunities WHERE run_id=?"
        args = [run_id]
        if strategy:
            q += " AND strategy=?"
            args.append(strategy)
        return [json.loads(r[0]) for r in self.db.execute(q + " ORDER BY tick", args)]

    def ledgers(self, run_id):
        return {s: json.loads(d) for s, d in self.db.execute(
            "SELECT strategy, data FROM ledgers WHERE run_id=?", (run_id,))}

    def latest_run(self, mode=None):
        q = "SELECT run_id FROM runs" + (" WHERE mode=?" if mode else "") + " ORDER BY started DESC LIMIT 1"
        r = self.db.execute(q, (mode,) if mode else ()).fetchone()
        return r[0] if r else None

    def run_info(self, run_id):
        r = self.db.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
        return None if not r else dict(zip(("run_id", "started", "mode", "seed", "source_run", "args"), r))

    def tick_stats(self, run_id):
        return self.db.execute(
            "SELECT strategy, COUNT(*), AVG(seconds), SUM(error IS NOT NULL) FROM ticks "
            "WHERE run_id=? GROUP BY strategy", (run_id,)).fetchall()

    def error_rows(self, run_id):
        return [json.loads(r[0]) for r in self.db.execute(
            "SELECT data FROM errors WHERE run_id=?", (run_id,))]

    def close(self):
        self.db.commit()
        self.db.close()
