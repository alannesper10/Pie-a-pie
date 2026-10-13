"""Caché histórica incremental (lab_data/history.sqlite, fuera de git).

Nunca vuelve a descargar lo que ya tiene: para cada (fuente, símbolo, marco)
guarda la cobertura [min_ts, max_ts] y solo pide lo que falta antes o después.
Las fuentes reales se inyectan como funciones `fetch(since_ms, until_ms)` que
devuelven [(ts_ms, open, high, low, close, volume)].
"""

import sqlite3
import time
from pathlib import Path
from typing import Callable, List, Optional, Tuple

Bar = Tuple[int, float, float, float, float, float]

SCHEMA = """
CREATE TABLE IF NOT EXISTS bars (source TEXT, symbol TEXT, tf TEXT, ts INTEGER,
    o REAL, h REAL, l REAL, c REAL, v REAL, PRIMARY KEY (source, symbol, tf, ts));
CREATE TABLE IF NOT EXISTS coverage (source TEXT, symbol TEXT, tf TEXT,
    min_ts INTEGER, max_ts INTEGER, updated REAL, PRIMARY KEY (source, symbol, tf));
CREATE TABLE IF NOT EXISTS fetch_log (source TEXT, symbol TEXT, tf TEXT, since INTEGER,
    until INTEGER, rows INTEGER, error TEXT, at REAL);
"""

TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000,
         "4h": 14_400_000, "1d": 86_400_000}


class HistoryCache:
    def __init__(self, path=Path("lab_data") / "history.sqlite"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.executescript(SCHEMA)

    def coverage(self, source, symbol, tf):
        r = self.db.execute("SELECT min_ts, max_ts FROM coverage WHERE source=? AND symbol=? AND tf=?",
                            (source, symbol, tf)).fetchone()
        return r if r else (None, None)

    def _store(self, source, symbol, tf, bars: List[Bar]):
        self.db.executemany("INSERT OR REPLACE INTO bars VALUES (?,?,?,?,?,?,?,?,?)",
                            [(source, symbol, tf, int(b[0]), *map(float, b[1:6])) for b in bars])
        lo, hi = self.coverage(source, symbol, tf)
        ts = [int(b[0]) for b in bars]
        if ts:
            lo = min(ts + ([lo] if lo is not None else []))
            hi = max(ts + ([hi] if hi is not None else []))
            self.db.execute("INSERT OR REPLACE INTO coverage VALUES (?,?,?,?,?,?)",
                            (source, symbol, tf, lo, hi, time.time()))
        self.db.commit()

    def ensure(self, source, symbol, tf, since_ms, until_ms,
               fetch: Callable[[int, int], List[Bar]]) -> dict:
        """Garantiza cobertura [since, until]; descarga SOLO los tramos faltantes."""
        step = TF_MS.get(tf, 3_600_000)
        lo, hi = self.coverage(source, symbol, tf)
        gaps = []
        if lo is None:
            gaps.append((since_ms, until_ms))
        else:
            if since_ms < lo - step:
                gaps.append((since_ms, lo - 1))
            if until_ms > hi + step:
                gaps.append((hi + 1, until_ms))
        fetched, errors = 0, []
        for a, b in gaps:
            try:
                bars = fetch(a, b)
                self._store(source, symbol, tf, bars)
                fetched += len(bars)
                err = None
            except Exception as e:  # noqa: BLE001 - se registra, no se inventa
                err = f"{type(e).__name__}: {str(e)[:200]}"
                errors.append(err)
            self.db.execute("INSERT INTO fetch_log VALUES (?,?,?,?,?,?,?,?)",
                            (source, symbol, tf, a, b, fetched, err, time.time()))
            self.db.commit()
        return {"gaps": gaps, "fetched": fetched, "errors": errors}

    def bars(self, source, symbol, tf, since_ms=0, until_ms=None) -> List[Bar]:
        until_ms = until_ms if until_ms is not None else 2**62
        return self.db.execute(
            "SELECT ts, o, h, l, c, v FROM bars WHERE source=? AND symbol=? AND tf=? "
            "AND ts BETWEEN ? AND ? ORDER BY ts", (source, symbol, tf, since_ms, until_ms)).fetchall()

    def closes(self, source, symbol, tf, since_ms=0, until_ms=None):
        return {ts: c for ts, _, _, _, c, _ in self.bars(source, symbol, tf, since_ms, until_ms)}

    def close(self):
        self.db.close()


# ------------------------------------------------------------- fetchers reales

def ccxt_fetcher(exchange, symbol, tf="1h", page=1000):
    """Paginado de OHLCV público vía ccxt (sin claves)."""
    step = TF_MS[tf]

    def fetch(since, until):
        out, cursor = {}, since
        for _ in range(1000):
            rows = exchange.fetch_ohlcv(symbol, tf, since=cursor, limit=page)
            fresh = [r for r in rows if r[0] not in out and r[0] <= until]
            if not fresh:
                break
            out.update({r[0]: r for r in fresh})
            last = max(r[0] for r in fresh)
            if last + step > until or last + 1 <= cursor:
                break
            cursor = last + 1
        return [tuple(out[k][:6]) for k in sorted(out)]
    return fetch


def yahoo_fetcher(ticker, tf="1d", session=None):
    """Velas de Yahoo Finance (chart v8, público). Son cierres, NO precios
    ejecutables: sirven para investigación estadística, no para arbitraje."""
    import requests
    s = session or requests.Session()
    interval = {"1d": "1d", "1h": "60m"}[tf]

    def fetch(since, until):
        r = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
                  params={"period1": since // 1000, "period2": until // 1000, "interval": interval},
                  headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        r.raise_for_status()
        res = (r.json().get("chart") or {}).get("result") or []
        if not res:
            return []
        ts = res[0].get("timestamp") or []
        q = (res[0].get("indicators") or {}).get("quote", [{}])[0]
        out = []
        for i, t in enumerate(ts):
            c = (q.get("close") or [None])[i]
            if c is None:
                continue
            out.append((t * 1000, q["open"][i] or c, q["high"][i] or c, q["low"][i] or c, c,
                        (q.get("volume") or [0])[i] or 0))
        return out
    return fetch
