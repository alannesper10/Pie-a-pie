"""P4: carry de divisas G10 con tasas reales (FRED), mensual.

Regla FIJA (registrada en AUDITORIA_ALCANCE_2026-10-16.md, P4; detalles de datos
fijados el 16/10 antes de ver resultados):
  - 9 monedas contra USD: EUR, JPY, GBP, AUD, CAD, CHF, NZD, NOK, SEK
  - ranking por la tasa interbancaria a 3 meses (OECD vía FRED) del mes m−2
    (sin mirar el futuro: la media mensual se publica con rezago)
  - largo las 2 de mayor tasa y corto las 2 de menor tasa, 25% de peso cada una
    (1x bruto, neutral al dólar, SIN apalancamiento)
  - retorno de una posición larga en c durante el mes m:
        spot (USD por unidad de c, fin de m / fin de m−1) − 1 + (i_c − i_usd)/1200
    con las tasas del mes m−1 (puntos forward); el corto es el negativo
  - una tasa con más de 2 meses de antigüedad excluye la moneda ese mes
  - costos: 2 pb por unidad de rotación de pesos + 0,5% anual sobre el bruto (SUPUESTO)
  - muestra 2002-05..2015 / fuera 2016..2026; métricas mensuales no solapadas
Benchmark estricto: la garantía no rinde (cuenta chica) -> se exige superar
también a la letra del Tesoro.
"""

import math

FX = {  # serie FRED, True si la serie es USD por unidad de la moneda
    "EUR": ("DEXUSEU", True), "JPY": ("DEXJPUS", False), "GBP": ("DEXUSUK", True),
    "AUD": ("DEXUSAL", True), "CAD": ("DEXCAUS", False), "CHF": ("DEXSZUS", False),
    "NZD": ("DEXUSNZ", True), "NOK": ("DEXNOUS", False), "SEK": ("DEXSDUS", False)}
RATES = {"USD": "IR3TIB01USM156N", "EUR": "IR3TIB01EZM156N", "JPY": "IR3TIB01JPM156N",
         "GBP": "IR3TIB01GBM156N", "AUD": "IR3TIB01AUM156N", "CAD": "IR3TIB01CAM156N",
         "CHF": "IR3TIB01CHM156N", "NZD": "IR3TIB01NZM156N", "NOK": "IR3TIB01NOM156N",
         "SEK": "IR3TIB01SEM156N"}
K = 2
COST_TURNOVER = 0.0002
MARKUP_YR = 0.005


def months_back(ym, k):
    y, m = map(int, ym.split("-"))
    m -= k
    while m <= 0:
        m += 12
        y -= 1
    return f"{y:04d}-{m:02d}"


def rate(rates, cur, ym, max_age=2):
    """Tasa del mes ym; si falta, la última de hasta max_age meses antes; si no, None."""
    for k in range(max_age + 1):
        v = rates.get(cur, {}).get(months_back(ym, k))
        if v is not None:
            return v
    return None


def run(spot_eom, rates, cost_mult=1.0):
    """spot_eom: {moneda: {AAAA-MM: USD por unidad, fin de mes}}; rates: {moneda: {AAAA-MM: %}}.
    -> lista de (AAAA-MM, retorno neto, pesos)."""
    months = sorted(set.intersection(*[set(v) for v in spot_eom.values()]))
    out, prev_w = [], {}
    for i in range(1, len(months)):
        m, pm = months[i], months[i - 1]
        rk = {c: rate(rates, c, months_back(m, 2)) for c in FX}
        rk = {c: v for c, v in rk.items() if v is not None}
        usd_now = rate(rates, "USD", months_back(m, 1))
        if len(rk) < 2 * K or usd_now is None:
            out.append((m, 0.0, {}))
            prev_w = {}
            continue
        order = sorted(rk, key=lambda c: rk[c])
        w = {c: -1.0 / (2 * K) for c in order[:K]}
        w.update({c: 1.0 / (2 * K) for c in order[-K:]})
        r = 0.0
        for c, wt in w.items():
            ic = rate(rates, c, months_back(m, 1))
            if ic is None:
                continue
            r += wt * (spot_eom[c][m] / spot_eom[c][pm] - 1 + (ic - usd_now) / 1200)
        turnover = sum(abs(w.get(c, 0) - prev_w.get(c, 0)) for c in set(w) | set(prev_w))
        r -= cost_mult * (turnover * COST_TURNOVER + sum(abs(x) for x in w.values()) * MARKUP_YR / 12)
        out.append((m, r, w))
        prev_w = w
    return out


def stats(rets, tbill_month=None):
    x = [r for _, r, w in rets if w]
    n = len(x)
    if n < 2:
        return {"n": n}
    m = sum(x) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1))
    eq, peak, mdd = 1.0, 1.0, 0.0
    for v in x:
        eq *= 1 + v
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    out = {"n": n, "ann_return_pct": ((eq) ** (12 / n) - 1) * 100, "t": m / (sd / math.sqrt(n)),
           "sharpe": m / sd * math.sqrt(12), "max_drawdown_pct": mdd * 100, "total_pct": (eq - 1) * 100,
           "worst_month_pct": min(x) * 100}
    if tbill_month:
        ex = [r - tbill_month(mm) for mm, r, w in rets if w]
        me = sum(ex) / n
        sde = math.sqrt(sum((v - me) ** 2 for v in ex) / (n - 1))
        out.update({"excess_vs_tbill_ann_pct": me * 12 * 100, "t_excess_vs_tbill": me / (sde / math.sqrt(n))})
    return out


# ---------------- datos (FRED) ----------------

def fred_series(sid, s):
    txt = s.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": sid}, timeout=60).text
    out = {}
    for line in txt.strip().splitlines()[1:]:
        d, v = line.split(",")
        if v not in (".", ""):
            out[d] = float(v)
    return out


def load(s):
    spot = {}
    for c, (sid, usd_per) in FX.items():
        daily = fred_series(sid, s)
        eom = {}
        for d in sorted(daily):
            eom[d[:7]] = daily[d] if usd_per else 1 / daily[d]    # último dato del mes
        spot[c] = eom
    rates = {c: {d[:7]: v for d, v in fred_series(sid, s).items()} for c, sid in RATES.items()}
    return spot, rates
