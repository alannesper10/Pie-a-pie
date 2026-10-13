"""Diagnóstico de los casos Polymarket NO_BOOK_FOR_LEG (solo lectura).

Para cada caso: qué pata faltó, por qué (recorte por tope, 404, error de red,
token nunca pedido) y qué decía el top of book de Gamma (indicativo, NO
ejecutable: Gamma no da profundidad). LIBRO_SIN_ASKS es un dato real: nadie
vendía NO en ese momento (la pata no se puede comprar). Los libros de ese momento NO se pueden
recuperar después: el CLOB solo sirve el libro actual. Estos casos quedan como
NO_RECUPERABLE; la evidencia nueva sale de recolecciones con libros completos.
"""

from collections import Counter

from ..modules.prediction import NEAR_MISS_GROSS, _f, candidate_legs, select_tokens

OLD_MAX_BOOKS = 200      # tope que tenía PolymarketSource hasta esta corrección


def leg_cause(token, snap_books, requested, errors_by_token, cap=OLD_MAX_BOOKS):
    if token in snap_books:
        return "PRESENTE" if (snap_books[token] or {}).get("asks") else "LIBRO_SIN_ASKS"
    if token not in requested:
        return "NUNCA_PEDIDO"
    if requested.index(token) >= cap:
        return "RECORTADO_POR_TOPE"
    err = errors_by_token.get(token, "")
    if "404" in err:
        return "SIN_LIBRO_404"
    return "ERROR_RED" if err else "SIN_RESPUESTA"


def diagnose_snapshot(snap, cap=OLD_MAX_BOOKS):
    pm = snap.polymarket or {}
    books = pm.get("books", {})
    requested = list(dict.fromkeys(select_tokens(pm.get("events", []))))
    errs = {e.get("token"): e.get("error", "") for e in snap.errors
            if e.get("venue") == "polymarket" and e.get("token")}
    out = []
    for e in pm.get("events", []):
        legs = candidate_legs(e)
        if len(legs) < 2:
            continue
        gross_top = sum(_f(m["bestBid"]) for m in legs) - 1
        if gross_top <= NEAR_MISS_GROSS:
            continue
        causes = [(m["tokens"][1], leg_cause(m["tokens"][1], books, requested, errs, cap))
                  for m in legs]
        missing = [(t, c) for t, c in causes if c != "PRESENTE"]
        if not missing:
            continue
        out.append({
            "tick": snap.tick, "ts": snap.ts, "key": f"polymarket|{e.get('slug')}",
            "k": len(legs), "missing": [{"token": t, "cause": c} for t, c in missing],
            "n_missing": len(missing),
            # indicativo: suma de bestBid YES (Gamma) - 1; sin profundidad ni fees
            "gross_top_gamma_indicative": gross_top,
            "status": "NO_RECUPERABLE"})
    return out


def diagnose_run(snapshots, cap=OLD_MAX_BOOKS):
    cases = []
    for s in snapshots:
        cases.extend(diagnose_snapshot(s, cap))
    causes = Counter(m["cause"] for c in cases for m in c["missing"])
    by_event = {}
    for c in cases:
        d = by_event.setdefault(c["key"], {"cases": 0, "ticks": [], "max_gross_gamma": None,
                                           "missing_legs": set()})
        d["cases"] += 1
        d["ticks"].append(c["tick"])
        g = c["gross_top_gamma_indicative"]
        d["max_gross_gamma"] = g if d["max_gross_gamma"] is None else max(d["max_gross_gamma"], g)
        d["missing_legs"].update(m["token"] for m in c["missing"])
    for d in by_event.values():
        d["missing_legs"] = sorted(d["missing_legs"])
        d["first_tick"], d["last_tick"] = min(d["ticks"]), max(d["ticks"])
        del d["ticks"]
    return {"cases": len(cases), "causes_by_leg": dict(causes),
            "events": len(by_event), "by_event": by_event,
            "gamma_positive_indicative": sum(1 for c in cases if c["gross_top_gamma_indicative"] > 0),
            "detail": cases}
