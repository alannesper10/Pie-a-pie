"""P6 (BIBLIOTECA_INTEGRADA_2026-10-16.md, especificación registrada en 9f248c5):
sesgo favorito/longshot en Polymarket.

Mercados binarios resueltos (volumen ≥ US$100.000, fin 01/2024–09/2026). Para cada
token: último precio del historial diario al menos 7 días antes de endDate; se
compra si 0,85 ≤ p ≤ 0,97 a p + 0,005 (medio spread SUPUESTO) más la comisión
C·rate·p·(1−p) si feesEnabled. Pago 1/0. Unidad estadística: el evento.
"""

import json
import math
from datetime import datetime, timezone

LO, HI = 0.85, 0.97
HALF_SPREAD = 0.005
DAYS_BEFORE = 7


def ts(x):
    return datetime.fromisoformat(x.replace("Z", "+00:00").replace(" ", "T").replace("+00", "+00:00")
                                  if x.endswith("+00") else x.replace("Z", "+00:00"))


def signal_price(history, end_dt, days_before=DAYS_BEFORE):
    """Último punto del historial con t ≤ end − days_before (sin mirar el futuro)."""
    cut = end_dt.timestamp() - days_before * 86400
    pts = [h for h in history if h["t"] <= cut]
    return pts[-1]["p"] if pts else None


def trade(market, histories, cost_mult=1.0):
    """-> lista de operaciones (una por token que cumple la señal)."""
    outs = json.loads(market["outcomes"]) if isinstance(market["outcomes"], str) else market["outcomes"]
    prices = json.loads(market["outcomePrices"]) if isinstance(market["outcomePrices"], str) else market["outcomePrices"]
    toks = json.loads(market["clobTokenIds"]) if isinstance(market["clobTokenIds"], str) else market["clobTokenIds"]
    if len(outs) != 2 or sorted(float(x) for x in prices) != [0.0, 1.0]:
        return []                                           # no binario o anulado: excluido
    end = ts(market["endDate"])
    closed = ts(market["closedTime"]) if market.get("closedTime") else end
    rate = 0.0
    if market.get("feesEnabled"):
        fs = market.get("feeSchedule") or {}
        rate = float(fs.get("rate") or 0.05)
    out = []
    for tok, won in zip(toks, prices):
        h = histories.get(tok)
        if not h:
            continue
        p = signal_price(h, end)
        if p is None or not (LO <= p <= HI):
            continue
        cost = p + cost_mult * HALF_SPREAD + cost_mult * rate * p * (1 - p)
        pay = float(won)
        out.append({"market": market.get("id"), "event": market.get("event_key"), "p": p, "cost": cost,
                    "won": pay == 1.0, "ret_pct": (pay - cost) / cost * 100,
                    "days": max((closed - end).total_seconds() / 86400 + DAYS_BEFORE, 1.0),
                    "closed": closed.strftime("%Y-%m-%d"), "category": market.get("category_key")})
    return out


def by_event(trades):
    ev = {}
    for t in trades:
        ev.setdefault(t["event"] or t["market"], []).append(t)
    return [{"event": k, "ret_pct": sum(x["ret_pct"] for x in v) / len(v),
             "days": max(x["days"] for x in v), "closed": max(x["closed"] for x in v),
             "category": v[0]["category"], "n": len(v)} for k, v in ev.items()]


def stats(events, tbill_pct_for):
    n = len(events)
    if n < 2:
        return {"n": n}
    ex = [e["ret_pct"] - tbill_pct_for(e["closed"], e["days"]) for e in events]
    m = sum(ex) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in ex) / (n - 1))
    rets = [e["ret_pct"] for e in events]
    return {"events": n, "mean_ret_pct": sum(rets) / n, "mean_excess_pct": m, "t": m / (sd / math.sqrt(n)),
            "losses": sum(r < 0 for r in rets), "worst_pct": min(rets)}
