"""Ventana horaria de recolección e integridad de una corrida guardada.

Ventana: la recolección de CCL corre solo durante la rueda (hora argentina,
UTC-3 fijo, sin horario de verano). Antes de la apertura espera; después
del cierre se detiene.

Integridad: cada captura se decodifica completa; se informan los ticks
faltantes, los huecos de tiempo, las capturas ilegibles y los errores de
fuentes por captura. Nada se rellena ni se interpola: un faltante queda
registrado como faltante.
"""

import json
import zlib
from datetime import datetime, timedelta, timezone

ART = timezone(timedelta(hours=-3))


def parse_window(spec):
    """'11:00-17:05' -> ((11, 0), (17, 5))."""
    a, b = spec.split("-")
    start = tuple(int(x) for x in a.split(":"))
    end = tuple(int(x) for x in b.split(":"))
    if start >= end:
        raise ValueError(f"ventana inválida: {spec}")
    return start, end


def window_bounds(now_utc, spec, day=None):
    """Inicio y fin (UTC) de la ventana del día argentino `day` (por defecto,
    el de `now_utc`)."""
    (h0, m0), (h1, m1) = parse_window(spec)
    day = day or now_utc.astimezone(ART).date()
    start = datetime(day.year, day.month, day.day, h0, m0, tzinfo=ART)
    end = datetime(day.year, day.month, day.day, h1, m1, tzinfo=ART)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)


def window_action(now_utc, spec, day=None):
    """-> ('wait', segundos) antes de la apertura, ('run', 0) dentro,
    ('stop', 0) después del cierre."""
    start, end = window_bounds(now_utc, spec, day)
    if now_utc < start:
        return "wait", (start - now_utc).total_seconds()
    if now_utc >= end:
        return "stop", 0.0
    return "run", 0.0


def _ts(x):
    try:
        return datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def last_valid_tick(db, run_id):
    """Último tick cuya captura se decodifica completa (-1 si ninguno).
    Una captura ilegible al final se vuelve a tomar al reanudar."""
    for tick, blob in db.execute("SELECT tick, data FROM snapshots WHERE run_id=? ORDER BY tick DESC",
                                 (run_id,)):
        try:
            json.loads(zlib.decompress(blob).decode())
            return tick
        except Exception:
            continue
    return -1


def verify_run(db, run_id, interval_sec=60, gap_factor=2.0, source="ccl"):
    """Revisa una corrida tick por tick (de a una captura, sin cargarla toda)."""
    rows = db.execute("SELECT tick, ts FROM snapshots WHERE run_id=? ORDER BY tick", (run_id,)).fetchall()
    out = {"run_id": run_id, "integrity_check": db.execute("PRAGMA integrity_check").fetchone()[0],
           "snapshots": len(rows), "first_ts": rows[0][1] if rows else None,
           "last_ts": rows[-1][1] if rows else None, "missing_ticks": [], "unreadable_ticks": [],
           "time_gaps": [], "ticks_with_errors": {}, "errors_by_source": {},
           f"ticks_without_{source}": []}
    if not rows:
        return out
    ticks = [t for t, _ in rows]
    out["missing_ticks"] = sorted(set(range(ticks[0], ticks[-1] + 1)) - set(ticks))
    prev = None
    for tick, ts in rows:
        cur = _ts(ts)
        if prev and cur and (cur - prev).total_seconds() > interval_sec * gap_factor:
            out["time_gaps"].append({"after_tick": tick - 1, "tick": tick, "from": prev.isoformat(),
                                     "to": cur.isoformat(), "seconds": (cur - prev).total_seconds()})
        prev = cur or prev
        (blob,) = db.execute("SELECT data FROM snapshots WHERE run_id=? AND tick=?", (run_id, tick)).fetchone()
        try:
            snap = json.loads(zlib.decompress(blob).decode())
        except Exception:
            out["unreadable_ticks"].append(tick)
            continue
        errs = snap.get("errors") or []
        if errs:
            out["ticks_with_errors"][tick] = [f"{e.get('venue')}:{e.get('what')}" for e in errs]
            for e in errs:
                k = f"{e.get('venue')}:{e.get('what')}"
                out["errors_by_source"][k] = out["errors_by_source"].get(k, 0) + 1
        if not snap.get(source):
            out[f"ticks_without_{source}"].append(tick)
    out["ok"] = (out["integrity_check"] == "ok" and not out["missing_ticks"]
                 and not out["unreadable_ticks"])
    return out
