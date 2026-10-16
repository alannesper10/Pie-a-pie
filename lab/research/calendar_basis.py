"""P2: spread perpetuo contra trimestral (Binance USDⓈ-M), mantenido hasta el vencimiento.

Mecanismo: el trimestral liquida contra el índice al vencer (entrega publicada
por Binance). El perpetuo sigue al índice vía funding. Si la base anualizada
del trimestral supera al funding esperado del perpetuo, vender el trimestral
y comprar el perpetuo (misma cantidad) captura la diferencia, neutral al
precio. El largo perpetuo PAGA el funding real del período.

Regla FIJA (registrada en reports/lab/AUDITORIA_ALCANCE_2026-10-16.md, P2):
  base_anual = (F/P − 1) · 365/días_al_vencimiento
  funding_30d_anual = media diaria del funding de 30 días · 365
  entrar si base_anual − funding_30d_anual > 3%; mantener hasta el vencimiento;
  una posición por activo a la vez (operaciones NO solapadas).
Costos: taker 0,05% por pata (VERIFICADO, Binance USDⓈ-M) + 2 pb de medio
spread/deslizamiento por pata (SUPUESTO) + 0,05% de entrega (SUPUESTO,
igual que lab/research/carry). Capital = nominal de UNA pata (cada pata con
margen del 50%, 2x: SUPUESTO). Comparación contra la letra del Tesoro del
mismo plazo. Separación: vencimientos ≤ 2023 (muestra) / ≥ 2024 (fuera).
"""

import math
from datetime import datetime, timezone

TAKER = 0.0005
SLIP = 0.0002
DELIVERY_FEE = 0.0005
THRESHOLD = 0.03
DAY = 86_400_000


def _d(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")


def trades(q_close, p_close, funding_day, deliveries, cost_mult=1.0, threshold=THRESHOLD, perp_at_delivery=None):
    """q_close/p_close: {día ISO: cierre} (vela diaria con apertura 00:00 UTC);
    funding_day: {día: suma del funding de ese día}; deliveries: {ms de entrega: precio};
    perp_at_delivery: {ms de entrega: precio del perpetuo a esa hora}. El perpetuo
    se cierra A LA HORA DE LA ENTREGA (08:00 UTC): cerrarlo al cierre del día deja
    una pata sin cobertura 16 horas (error corregido el 16/10).
    -> lista de operaciones cerradas (una por vencimiento como mucho)."""
    exps = sorted(deliveries)
    days = sorted(set(q_close) & set(p_close))
    out, busy_until = [], None
    for day in days:
        t = datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000 + DAY  # cierre de la vela
        if busy_until and t <= busy_until:
            continue
        exp = next((e for e in exps if e > t + DAY), None)    # al menos 1 día al vencimiento
        if exp is None:
            continue
        dte = (exp - t) / DAY
        if dte > 100:                                          # la serie continua aún no es este contrato
            continue
        f0, p0 = q_close[day], p_close[day]
        past = [funding_day[x] for x in sorted(funding_day) if x <= day][-30:]
        if len(past) < 30:
            continue
        basis_ann = (f0 / p0 - 1) * 365 / dte
        fund_ann = sum(past) / len(past) * 365
        if basis_ann - fund_ann <= threshold:
            continue
        exp_day = _d(exp)
        hold = [x for x in sorted(funding_day) if day < x <= exp_day]
        p_exit = (perp_at_delivery or {}).get(exp)
        if not hold or p_exit is None:
            continue                                  # sin precio del perpetuo a la hora de entrega: no se inventa
        d_px = deliveries[exp]
        # por unidad de activo: corto trimestral + largo perpetuo
        gross = (f0 - d_px) + (p_exit - p0)
        funding_paid = sum(funding_day[x] for x in hold) * p0          # el largo paga funding (aprox. con P0)
        c = cost_mult * (2 * (TAKER + SLIP) * p0 + (TAKER + SLIP) * p_exit + DELIVERY_FEE * d_px)
        capital = p0
        net = gross - funding_paid - c
        # peor marca del spread durante la tenencia (con el cierre diario del trimestral)
        mtm = [((f0 - q_close[x]) + (p_close[x] - p0)) / capital for x in sorted(q_close)
               if day < x < exp_day and x in p_close]
        out.append({"entry": day, "expiry": exp_day, "days": dte, "basis_ann": basis_ann, "fund_ann": fund_ann,
                    "gross_pct": gross / capital * 100, "funding_pct": funding_paid / capital * 100,
                    "costs_pct": c / capital * 100, "net_pct": net / capital * 100,
                    "delivery_vs_perp_pct": (d_px / p_exit - 1) * 100,
                    "worst_mtm_pct": min(mtm) * 100 if mtm else 0.0})
        busy_until = exp
    return out


def evaluate(tr, tbill_pct_for):
    """Agrega exceso sobre la letra por operación y t sobre operaciones (no solapadas)."""
    if not tr:
        return {"n": 0}
    ex = [t["net_pct"] - tbill_pct_for(t["entry"], t["days"]) for t in tr]
    n = len(ex)
    m = sum(ex) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in ex) / (n - 1)) if n > 1 else float("nan")
    return {"n": n, "mean_net_pct": sum(t["net_pct"] for t in tr) / n, "mean_excess_pct": m,
            "t_excess": m / (sd / math.sqrt(n)) if n > 1 and sd > 0 else None,
            "positive_excess": sum(x > 0 for x in ex), "worst_net_pct": min(t["net_pct"] for t in tr),
            "worst_mtm_pct": min(t["worst_mtm_pct"] for t in tr)}


# ---------------- datos (públicos) ----------------

def fetch(pair, session=None):
    import requests
    s = session or requests.Session()
    dl = s.get("https://fapi.binance.com/futures/data/delivery-price", params={"pair": pair}, timeout=30).json()
    deliveries = {x["deliveryTime"] + 8 * 3_600_000: float(x["deliveryPrice"]) for x in dl}
    # deliveryTime viene a las 00:00 del día de entrega; la entrega es a las 08:00 UTC

    def kl(url, params):
        out, start = {}, 1577836800000
        while True:
            rows = s.get(url, params={**params, "interval": "1d", "startTime": start, "limit": 1500}, timeout=30).json()
            if not rows or not isinstance(rows, list):
                break
            for r in rows:
                out[_d(r[0])] = float(r[4])
            start = rows[-1][0] + DAY
            if len(rows) < 1500:
                break
        return out
    q = kl("https://fapi.binance.com/fapi/v1/continuousKlines", {"pair": pair, "contractType": "CURRENT_QUARTER"})
    p = kl("https://fapi.binance.com/fapi/v1/klines", {"symbol": pair})
    fd, start = {}, 1577836800000
    while True:
        rows = s.get("https://fapi.binance.com/fapi/v1/fundingRate",
                     params={"symbol": pair, "startTime": start, "limit": 1000}, timeout=30).json()
        if not rows:
            break
        for r in rows:
            k = _d(r["fundingTime"])
            fd[k] = fd.get(k, 0.0) + float(r["fundingRate"])
        start = rows[-1]["fundingTime"] + 1
        if len(rows) < 1000:
            break
    pd = {}
    for exp in deliveries:
        rows = s.get("https://fapi.binance.com/fapi/v1/klines",
                     params={"symbol": pair, "interval": "1h", "startTime": exp, "limit": 1}, timeout=30).json()
        if rows and rows[0][0] == exp:
            pd[exp] = float(rows[0][1])           # apertura de la vela de las 08:00 = precio a la hora de entrega
    return q, p, fd, deliveries, pd
