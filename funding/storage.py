"""SQLite local para funding/basis (funding_data/, fuera de git)."""

import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS funding_history (
    exchange TEXT, asset TEXT, ts INTEGER, rate REAL,
    PRIMARY KEY (exchange, asset, ts));
CREATE TABLE IF NOT EXISTS price_history (
    exchange TEXT, asset TEXT, market TEXT, ts INTEGER, close REAL,
    PRIMARY KEY (exchange, asset, market, ts));
CREATE TABLE IF NOT EXISTS snapshots (
    ts TEXT, exchange TEXT, asset TEXT,
    spot_bid REAL, spot_ask REAL, perp_bid REAL, perp_ask REAL,
    mark REAL, index_price REAL, funding_rate REAL, funding_interval_h REAL,
    next_funding_ts INTEGER, basis_pct REAL, spot_depth_usd REAL,
    perp_depth_usd REAL, expected_net_pct REAL, cost_pct REAL, detail TEXT);
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, exchange TEXT, asset TEXT,
    opened_at TEXT, closed_at TEXT, snapshots INTEGER,
    max_expected_net_pct REAL, last_expected_net_pct REAL,
    max_size_usd REAL, detail TEXT);
CREATE TABLE IF NOT EXISTS paper_events (
    ts TEXT, exchange TEXT, asset TEXT, event TEXT, detail TEXT);
CREATE TABLE IF NOT EXISTS errors (
    ts TEXT, exchange TEXT, endpoint TEXT, error TEXT);
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
"""


class Storage:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    # -- historial ---------------------------------------------------------
    def save_funding(self, exchange, asset, rows):
        self.db.executemany(
            "INSERT OR REPLACE INTO funding_history VALUES (?,?,?,?)",
            [(exchange, asset, int(ts), float(rate)) for ts, rate in rows])
        self.db.commit()

    def load_funding(self, exchange, asset, since_ms=0):
        cur = self.db.execute(
            "SELECT ts, rate FROM funding_history WHERE exchange=? AND asset=? "
            "AND ts>=? ORDER BY ts", (exchange, asset, since_ms))
        return cur.fetchall()

    def save_prices(self, exchange, asset, market, rows):
        self.db.executemany(
            "INSERT OR REPLACE INTO price_history VALUES (?,?,?,?,?)",
            [(exchange, asset, market, int(ts), float(c)) for ts, c in rows])
        self.db.commit()

    def load_prices(self, exchange, asset, market, since_ms=0):
        cur = self.db.execute(
            "SELECT ts, close FROM price_history WHERE exchange=? AND asset=? "
            "AND market=? AND ts>=? ORDER BY ts", (exchange, asset, market, since_ms))
        return cur.fetchall()

    # -- vivo --------------------------------------------------------------
    def save_snapshot(self, s: dict):
        cols = ["ts", "exchange", "asset", "spot_bid", "spot_ask", "perp_bid",
                "perp_ask", "mark", "index_price", "funding_rate",
                "funding_interval_h", "next_funding_ts", "basis_pct",
                "spot_depth_usd", "perp_depth_usd", "expected_net_pct",
                "cost_pct", "detail"]
        self.db.execute(f"INSERT INTO snapshots VALUES ({','.join('?' * len(cols))})",
                        [s.get(c) if c != "detail" else json.dumps(s.get(c, {}))
                         for c in cols])
        self.db.commit()

    def open_opportunity(self, exchange, asset, ts, net_pct, size_usd, detail):
        cur = self.db.execute(
            "INSERT INTO opportunities (exchange, asset, opened_at, snapshots, "
            "max_expected_net_pct, last_expected_net_pct, max_size_usd, detail) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (exchange, asset, ts, 1, net_pct, net_pct, size_usd, json.dumps(detail)))
        self.db.commit()
        return cur.lastrowid

    def update_opportunity(self, opp_id, net_pct, size_usd):
        self.db.execute(
            "UPDATE opportunities SET snapshots=snapshots+1, "
            "max_expected_net_pct=MAX(max_expected_net_pct, ?), "
            "last_expected_net_pct=?, max_size_usd=MAX(max_size_usd, ?) WHERE id=?",
            (net_pct, net_pct, size_usd, opp_id))
        self.db.commit()

    def close_opportunity(self, opp_id, ts):
        self.db.execute("UPDATE opportunities SET closed_at=? WHERE id=?", (ts, opp_id))
        self.db.commit()

    def open_opportunity_id(self, exchange, asset):
        row = self.db.execute(
            "SELECT id FROM opportunities WHERE exchange=? AND asset=? AND "
            "closed_at IS NULL ORDER BY id DESC LIMIT 1", (exchange, asset)).fetchone()
        return row[0] if row else None

    def log_paper(self, ts, exchange, asset, event, detail):
        self.db.execute("INSERT INTO paper_events VALUES (?,?,?,?,?)",
                        (ts, exchange, asset, event, json.dumps(detail, default=str)))
        self.db.commit()

    def log_error(self, ts, exchange, endpoint, error):
        self.db.execute("INSERT INTO errors VALUES (?,?,?,?)",
                        (ts, exchange, endpoint, str(error)[:500]))
        self.db.commit()

    def get(self, k, default=None):
        row = self.db.execute("SELECT v FROM kv WHERE k=?", (k,)).fetchone()
        return json.loads(row[0]) if row else default

    def put(self, k, v):
        self.db.execute("INSERT OR REPLACE INTO kv VALUES (?,?)", (k, json.dumps(v)))
        self.db.commit()

    def count(self, table, where="1=1", params=()):
        return self.db.execute(f"SELECT COUNT(*) FROM {table} WHERE {where}",
                               params).fetchone()[0]
