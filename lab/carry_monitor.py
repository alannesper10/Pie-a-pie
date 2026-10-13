"""Monitor de cash-and-carry (solo observación; nunca opera).

Por cada futuro con vencimiento observado registra, por separado:
  esperado   rendimiento FIJADO al entrar (base menos costos estimados) y el
             exceso sobre la letra del Tesoro del mismo plazo (ex ante)
  observado  se completa solo cuando el contrato vence y se conoce el precio
             de entrega (resultado ex post de una entrada hipotética)
  riesgo     precio de liquidación del corto a 1x y 2x y la suba necesaria
La señal es la MISMA regla congelada del estudio histórico
(lab/research/carry.rule_eval): exceso ex ante > 0 a 1x. No se ajusta.
Registro en lab_data/carry_monitor.sqlite (fuera de git).
"""

import json
import sqlite3
from pathlib import Path

from .research import carry

DB = Path("lab_data") / "carry_monitor.sqlite"
SCHEMA = """CREATE TABLE IF NOT EXISTS obs (ts TEXT, key TEXT, venue TEXT, expiry_ms INTEGER,
    days REAL, spot_ask REAL, fut_bid REAL, basis_pct REAL, expected_net_1x_pct REAL,
    tbill_rate_pct REAL, tbill_period_pct REAL, ex_ante_excess_1x_pct REAL, signal INTEGER,
    liq_price_1x REAL, liq_price_2x REAL, rise_to_liq_1x_pct REAL, observed_net_1x_pct REAL,
    PRIMARY KEY (ts, key));"""


def evaluate(books, meta, now_ms, rate_pct):
    """Puro: libros y meta de FuturesSource -> filas del monitor."""
    rows = []
    for k, m in sorted(meta.items()):
        fb, sb = books.get(k), books.get(f"{m['venue']}|{m['spot']}")
        if not fb or not sb or not fb.get("bids") or not sb.get("asks"):
            continue
        s0, f0 = sb["asks"][0][0], fb["bids"][0][0]
        days = (m["expiry"] - now_ms) / 86_400_000
        if days <= 0:
            continue
        exp_net = carry.ex_ante_net(s0, f0) / (s0 + f0)
        tb = carry.tbill_period_return(rate_pct, days) if rate_pct is not None else None
        excess = exp_net - tb if tb is not None else None
        liq1 = (f0 + f0 / 1) / (1 + carry.MMR)
        liq2 = (f0 + f0 / 2) / (1 + carry.MMR)
        rows.append({"key": k, "venue": m["venue"], "expiry_ms": m["expiry"], "days": days,
                     "spot_ask": s0, "fut_bid": f0, "basis_pct": f0 / s0 - 1,
                     "expected_net_1x_pct": exp_net, "tbill_rate_pct": rate_pct,
                     "tbill_period_pct": tb, "ex_ante_excess_1x_pct": excess,
                     "signal": int(excess is not None and excess > 0),
                     "liq_price_1x": liq1, "liq_price_2x": liq2,
                     "rise_to_liq_1x_pct": liq1 / f0 - 1, "observed_net_1x_pct": None})
    return rows


def save(rows, ts, path=DB):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    cols = ["ts"] + list(rows[0].keys()) if rows else []
    for r in rows:
        db.execute(f"INSERT OR IGNORE INTO obs ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                   [ts] + list(r.values()))
    db.commit()
    db.close()


def settle(deliveries_by_venue_expiry, path=DB):
    """Completa el resultado OBSERVADO de las observaciones cuyo contrato ya
    venció: base fijada menos costos, con la venta del spot al precio de
    entrega (aproximación; el estudio histórico usa el TWAP real)."""
    db = sqlite3.connect(path)
    n = 0
    for (venue, expiry_ms), delivery in deliveries_by_venue_expiry.items():
        for ts, key, s0, f0 in db.execute("SELECT ts, key, spot_ask, fut_bid FROM obs WHERE venue=? AND "
                                          "expiry_ms=? AND observed_net_1x_pct IS NULL",
                                          (venue, expiry_ms)).fetchall():
            h = carry.hold_to_expiry(s0, f0, delivery, delivery)
            db.execute("UPDATE obs SET observed_net_1x_pct=? WHERE ts=? AND key=?",
                       (h["net"] / (s0 + f0), ts, key))
            n += 1
    db.commit()
    db.close()
    return n


def summary(path=DB):
    db = sqlite3.connect(path)
    r = db.execute("SELECT COUNT(*), SUM(signal), COUNT(DISTINCT ts), MAX(ex_ante_excess_1x_pct), "
                   "SUM(observed_net_1x_pct IS NOT NULL) FROM obs").fetchone()
    last = db.execute("SELECT MAX(ts) FROM obs").fetchone()[0]
    latest = [dict(zip(("key", "days", "basis_pct", "expected_net_1x_pct", "tbill_period_pct",
                        "ex_ante_excess_1x_pct", "signal", "rise_to_liq_1x_pct"), x)) for x in db.execute(
        "SELECT key, days, basis_pct, expected_net_1x_pct, tbill_period_pct, ex_ante_excess_1x_pct, signal, "
        "rise_to_liq_1x_pct FROM obs WHERE ts=? ORDER BY ex_ante_excess_1x_pct DESC", (last,))]
    db.close()
    return {"observations": r[0], "signals": r[1] or 0, "scans": r[2], "best_excess": r[3],
            "settled": r[4] or 0, "last_scan": last, "latest": latest,
            "rule": "exceso ex ante sobre la letra > 0 a 1x (congelada, lab/research/carry)"}


def scan_live(path=DB):
    import requests
    from datetime import datetime, timezone
    from .sources import FuturesSource
    books, meta, errs = FuturesSource().fetch()
    now = datetime.now(timezone.utc)
    rate = carry.rate_at(carry.fred_dtb3(requests.Session()), int(now.timestamp() * 1000))
    rows = evaluate(books, meta, int(now.timestamp() * 1000), rate)
    save(rows, now.isoformat(timespec="seconds"), path)
    return {"rows": len(rows), "signals": sum(r["signal"] for r in rows), "errors": errs,
            "summary": summary(path)}


if __name__ == "__main__":
    print(json.dumps(scan_live(), indent=1, default=str))
