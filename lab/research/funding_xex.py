"""P3: diferencia de funding del mismo perpetuo entre Binance y Bybit (neutral al precio).

Mecanismo: el mismo contrato (p. ej. BTCUSDT) paga funding distinto en cada
exchange. Corto en el exchange que paga más funding a los cortos (funding
más alto), largo en el otro: se cobra la diferencia sin exposición al precio,
salvo la diferencia de precio entre los dos perpetuos (se contabiliza).

Regla FIJA (16/10/2026, antes de ver resultados):
  dif7 = media de 7 días de (funding diario A − funding diario B) · 365
  abrir si |dif7| > 8%: corto donde el funding es mayor, largo donde es menor
  cerrar si |dif7| < 2%
Contabilidad diaria por unidad de nominal (un lado):
  + funding cobrado en el corto − funding pagado en el largo (tasas reales del día)
  + retorno del largo − retorno del corto (cierres diarios de cada perpetuo)
  − costos al abrir y cerrar: taker en 2 patas (Binance 0,05% y Bybit 0,055%,
    VERIFICADOS en las tablas oficiales) + 2 pb de deslizamiento por pata (SUPUESTO)
    + 1 USDT de transferencia por operación sobre US$1.000 (0,1%, SUPUESTO)
Capital = nominal de una pata (cada exchange con margen del 50%, 2x: SUPUESTO).
Comparación: exceso sobre la letra del Tesoro en los días con posición
(el capital ocioso rinde la letra igual en ambas alternativas).
Estadística: t sobre semanas no solapadas del exceso. Separación:
≤ 2023 muestra / ≥ 2024 fuera. 5 monedas → Bonferroni sobre 5 pruebas.
OKX no tiene historial público de funding de más de ~3 meses: queda fuera de la prueba.
"""

import math
from datetime import datetime, timezone

FEE = {"binance": 0.0005, "bybit": 0.00055}
SLIP = 0.0002
TRANSFER_PCT = 0.001
OPEN, CLOSE = 0.08, 0.02


def _d(ms):
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime("%Y-%m-%d")


def simulate(days, fa, fb, pa, pb, cost_mult=1.0):
    """days: lista ordenada de días con datos en ambos; fa/fb: funding diario
    (suma de las liquidaciones del día) en A (binance) y B (bybit); pa/pb: cierres.
    -> lista de (día, retorno neto sobre capital, en_posición)."""
    out, pos = [], 0          # pos = +1: corto en A, largo en B; −1: corto en B, largo en A
    entry_cost = cost_mult * (FEE["binance"] + FEE["bybit"] + 2 * SLIP)
    for i, d in enumerate(days):
        r = 0.0
        if i > 0 and pos != 0:
            prev = days[i - 1]
            ra, rb = pa[d] / pa[prev] - 1, pb[d] / pb[prev] - 1
            if pos == 1:          # corto A, largo B: cobra fa, paga fb
                r = fa[d] - fb[d] + (rb - ra)
            else:
                r = fb[d] - fa[d] + (ra - rb)
        # decisión al cierre del día d con datos hasta d (se aplica desde d+1)
        if i >= 7:
            dif = sum(fa[x] - fb[x] for x in days[i - 6:i + 1]) / 7 * 365
            if pos == 0 and abs(dif) > OPEN:
                pos = 1 if dif > 0 else -1
                r -= entry_cost + cost_mult * TRANSFER_PCT
            elif pos != 0 and abs(dif) < CLOSE:
                pos = 0
                r -= entry_cost
        out.append((d, r, pos != 0 or r != 0.0))
    return out


def weekly_excess(rets, tbill_daily):
    """Exceso sobre la letra solo en días con posición; sumas semanales no solapadas."""
    weeks, cur, k = [], 0.0, 0
    for d, r, active in rets:
        cur += (r - tbill_daily(d)) if active else 0.0
        k += 1
        if k == 7:
            weeks.append(cur)
            cur, k = 0.0, 0
    return weeks


def stats(weeks, rets):
    n = len(weeks)
    if n < 2:
        return {"weeks": n}
    m = sum(weeks) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in weeks) / (n - 1))
    eq, peak, mdd = 1.0, 1.0, 0.0
    for _, r, _ in rets:
        eq *= 1 + r
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    active = sum(1 for _, _, a in rets if a)
    trades = sum(1 for i in range(1, len(rets)) if rets[i][2] and not rets[i - 1][2])
    return {"weeks": n, "excess_total_pct": sum(weeks) * 100, "excess_week_mean_pct": m * 100,
            "t": m / (sd / math.sqrt(n)) if sd > 0 else None, "gross_total_pct": (eq - 1) * 100,
            "max_drawdown_pct": mdd * 100, "days_active": active, "trades": trades}


# ---------------- datos públicos ----------------

def binance(symbol, s):
    fr, start = {}, 1609459200000            # 2021-01-01
    while True:
        rows = s.get("https://fapi.binance.com/fapi/v1/fundingRate",
                     params={"symbol": symbol, "startTime": start, "limit": 1000}, timeout=30).json()
        if not rows:
            break
        for r in rows:
            fr[_d(r["fundingTime"])] = fr.get(_d(r["fundingTime"]), 0.0) + float(r["fundingRate"])
        start = rows[-1]["fundingTime"] + 1
        if len(rows) < 1000:
            break
    px, start = {}, 1609459200000
    while True:
        rows = s.get("https://fapi.binance.com/fapi/v1/klines",
                     params={"symbol": symbol, "interval": "1d", "startTime": start, "limit": 1500}, timeout=30).json()
        if not rows:
            break
        for r in rows:
            px[_d(r[0])] = float(r[4])
        start = rows[-1][0] + 86_400_000
        if len(rows) < 1500:
            break
    return fr, px


def bybit(symbol, s):
    fr, end = {}, None
    while True:
        params = {"category": "linear", "symbol": symbol, "limit": 200}
        if end:
            params["endTime"] = end
        rows = s.get("https://api.bybit.com/v5/market/funding/history", params=params, timeout=30).json()["result"]["list"]
        if not rows:
            break
        for r in rows:
            k = _d(r["fundingRateTimestamp"])
            fr[k] = fr.get(k, 0.0) + float(r["fundingRate"])
        oldest = min(int(r["fundingRateTimestamp"]) for r in rows)
        if oldest < 1609459200000 or len(rows) < 200:
            break
        end = oldest - 1
    px, end = {}, None
    while True:
        params = {"category": "linear", "symbol": symbol, "interval": "D", "limit": 1000}
        if end:
            params["end"] = end
        rows = s.get("https://api.bybit.com/v5/market/kline", params=params, timeout=30).json()["result"]["list"]
        if not rows:
            break
        for r in rows:
            px[_d(r[0])] = float(r[4])
        oldest = min(int(r[0]) for r in rows)
        if oldest < 1609459200000 or len(rows) < 1000:
            break
        end = oldest - 1
    return fr, px
