"""Episodios: una oportunidad que persiste varios ticks se cuenta UNA vez.

Para cada (estrategia, clave) se agrupan los ticks CONSECUTIVOS con neto
estimado > 0 en un episodio, con: primer y último momento, duración, cuántas
veces seguía ejecutable al verificarla (libros re-pedidos tras la latencia:
status FILLED) y el neto. Requiere una evaluación con ledger nuevo en cada
tick (`replay --fresh-ledger`): si no, el capital bloqueado en la primera
ejecución oculta la persistencia (NO_CAPITAL)."""

from datetime import datetime

from .research.stats import mean


def _secs(a, b):
    try:
        return (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds()
    except (TypeError, ValueError):
        return None


def build(opps, tick_ts=None):
    """opps: filas de LabStore.opportunities (dicts). tick_ts: {tick: ts} para
    medir la duración hasta el primer tick en que ya NO estaba."""
    by = {}
    for o in opps:
        if (o.get("net_estimated_usd") or 0) > 0 and o.get("stage") in ("ESTIMATED", "SIMULATED"):
            by.setdefault((o["strategy"], o["key"]), []).append(o)
    eps = []
    for (strategy, key), lst in by.items():
        lst.sort(key=lambda o: o["tick"])
        runs, cur = [], [lst[0]]
        for o in lst[1:]:
            if o["tick"] == cur[-1]["tick"] + 1:
                cur.append(o)
            else:
                runs.append(cur)
                cur = [o]
        runs.append(cur)
        for r in runs:
            filled = [o for o in r if (o.get("sim") or {}).get("status") == "FILLED"]
            end_ts = (tick_ts or {}).get(r[-1]["tick"] + 1, r[-1]["ts"])
            eps.append({
                "strategy": strategy, "key": key, "first_tick": r[0]["tick"],
                "last_tick": r[-1]["tick"], "ticks": len(r), "first_ts": r[0]["ts"],
                "last_ts": r[-1]["ts"], "duration_s_min": _secs(r[0]["ts"], r[-1]["ts"]),
                "duration_s_max": _secs(r[0]["ts"], end_ts),
                "executable_at_verification": len(filled),
                "net_estimated_mean": mean([o["net_estimated_usd"] for o in r]),
                "net_simulated_mean": mean([(o.get("sim") or {}).get("net_usd") or 0 for o in filled])
                if filled else None,
                "reasons": sorted({o.get("reason") or "" for o in r}),
                "categories": sorted({o.get("category") or o.get("classification") or "" for o in r})})
    eps.sort(key=lambda e: (e["strategy"], e["first_tick"]))
    return eps


def summarize(eps):
    out = {}
    for e in eps:
        d = out.setdefault(e["strategy"], {"episodes": 0, "with_executable_tick": 0,
                                           "ticks_positive": 0, "durations_s": []})
        d["episodes"] += 1
        d["with_executable_tick"] += e["executable_at_verification"] > 0
        d["ticks_positive"] += e["ticks"]
        if e["duration_s_min"] is not None:
            d["durations_s"].append(e["duration_s_min"])
    for d in out.values():
        ds = sorted(d.pop("durations_s"))
        d["duration_s_median"] = ds[len(ds) // 2] if ds else None
        d["duration_s_max"] = ds[-1] if ds else None
    return out
