"""E3 (BIBLIOTECA_INTEGRADA_2026-10-16.md, reglas registradas en ea6e551):
reversión de la base anualizada del trimestral contra el perpetuo (hipótesis
propia sobre Chan Ej. 5.4).

b_t = (F/P − 1)·365/días; z = (b_t − media20)/desvío20 (ventana que incluye t).
z > 1 -> vender trimestral, comprar perpetuo; z < −1 -> al revés.
Salida: z cruza 0 (cambia de signo respecto de la entrada) o quedan ≤ 3 días al vencimiento.
P&L diario por unidad de capital (nominal de una pata, al precio de entrada):
  lado +1 (corto Q / largo P): [−ΔQ + ΔP]/P_e − funding_t·P_{t−1}/P_e
  lado −1: el negativo (el corto perpetuo cobra el funding)
Costos: 0,05% + 2 pb por pata, al entrar y al salir (4 operaciones).
"""

import math
from datetime import datetime, timezone

COST = 0.0005 + 0.0002
LOOK = 20
EXIT_DTE = 3


def _ms(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000) + 86_400_000


def trades(q, p, fd, deliveries, cost=COST):
    exps = sorted(deliveries)
    days = sorted(set(q) & set(p))
    b, out, pos = {}, [], None
    for i, d in enumerate(days):
        t = _ms(d)
        exp = next((e for e in exps if e > t), None)
        if exp is None:
            continue
        dte = (exp - t) / 86_400_000
        if 0 < dte <= 100:
            b[d] = (q[d] / p[d] - 1) * 365 / dte
        if pos:                                   # actualizar la posición abierta
            prev = pos["last"]
            dq, dp = q[d] - q[prev], p[d] - p[prev]
            r = pos["side"] * ((-dq + dp) / pos["pe"] - fd.get(d, 0.0) * p[prev] / pos["pe"])
            pos["pnl"] += r
            pos["last"] = d
        hist = [b[x] for x in days[max(0, i - LOOK + 1):i + 1] if x in b]
        z = None
        if len(hist) == LOOK and d in b:
            m = sum(hist) / LOOK
            sd = math.sqrt(sum((x - m) ** 2 for x in hist) / (LOOK - 1))
            z = (b[d] - m) / sd if sd > 0 else None
        if pos:
            exit_now = dte <= EXIT_DTE or exp != pos["exp"] or (z is not None and z * pos["side"] <= 0)
            if exit_now:
                pos["pnl"] -= 2 * cost
                out.append({"entry": pos["entry"], "exit": d, "side": pos["side"], "net_pct": pos["pnl"] * 100,
                            "days": (datetime.fromisoformat(d) - datetime.fromisoformat(pos["entry"])).days})
                pos = None
                continue
        if pos is None and z is not None and dte > EXIT_DTE + 1 and abs(z) > 1:
            pos = {"side": 1 if z > 1 else -1, "entry": d, "last": d, "pe": p[d], "exp": exp, "pnl": -2 * cost}
    return out


def evaluate(tr, tbill_pct_for):
    if len(tr) < 2:
        return {"n": len(tr)}
    ex = [t["net_pct"] - tbill_pct_for(t["entry"], max(t["days"], 1)) for t in tr]
    n = len(ex)
    m = sum(ex) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in ex) / (n - 1))
    return {"n": n, "mean_net_pct": sum(t["net_pct"] for t in tr) / n, "mean_excess_pct": m,
            "t_excess": m / (sd / math.sqrt(n)) if sd > 0 else None,
            "win": sum(t["net_pct"] > 0 for t in tr), "worst_pct": min(t["net_pct"] for t in tr),
            "total_net_pct": sum(t["net_pct"] for t in tr), "mean_days": sum(t["days"] for t in tr) / n}
