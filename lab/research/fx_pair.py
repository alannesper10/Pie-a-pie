"""E4 (BIBLIOTECA_INTEGRADA_2026-10-16.md, reglas registradas en ea6e551): par AUD.CAD
con interés de rollover (Chan Ej. 5.2), estrategia lineal acotada.

AUDCAD = AUDUSD × USDCAD (FRED: DEXUSAL y 1/DEXCAUS, diarios).
z = (P − media20)/desvío20; posición en AUD (contra CAD) = −z/2 acotada a ±1 (1x).
Retorno diario = pos_{t−1}·(P_t/P_{t−1} − 1) + pos_{t−1}·(i_AUD − i_CAD)/365·días
                 − |Δpos|·2 pb − |pos|·0,5%/365·días
Tasas: interbancarias a 3 meses (OECD vía FRED) del mes anterior.
"""

import math

COST = 0.0002
MARKUP = 0.005
LOOK = 20


def run(dates, px, rate_aud, rate_cad, cost_mult=1.0):
    """dates ordenadas; px: {d: AUDCAD}; rate_*: función(d) -> % anual. -> [(d, ret)]"""
    from datetime import date
    out, pos = [], 0.0
    for i in range(1, len(dates)):
        d, p = dates[i], dates[i - 1]
        gap = (date.fromisoformat(d) - date.fromisoformat(p)).days
        r = pos * (px[d] / px[p] - 1)
        ra, rc = rate_aud(p), rate_cad(p)
        if ra is not None and rc is not None:
            r += pos * (ra - rc) / 100 / 365 * gap
        r -= cost_mult * abs(pos) * MARKUP / 365 * gap
        new = pos
        if i >= LOOK:
            win = [px[x] for x in dates[i - LOOK + 1:i + 1]]
            m = sum(win) / LOOK
            sd = math.sqrt(sum((v - m) ** 2 for v in win) / (LOOK - 1))
            if sd > 0:
                new = max(-1.0, min(1.0, -((px[d] - m) / sd) / 2))
        r -= cost_mult * abs(new - pos) * COST
        pos = new
        out.append((d, r))
    return out


def stats(rets, block=5):
    x = [r for _, r in rets]
    blocks = [sum(x[i:i + block]) for i in range(0, len(x) - block + 1, block)]
    n = len(blocks)
    m = sum(blocks) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in blocks) / (n - 1))
    eq, peak, mdd = 1.0, 1.0, 0.0
    for v in x:
        eq *= 1 + v
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    yrs = len(x) / 252
    return {"weeks": n, "t": m / (sd / math.sqrt(n)) if sd > 0 else None, "total_pct": (eq - 1) * 100,
            "ann_pct": (eq ** (1 / yrs) - 1) * 100, "max_drawdown_pct": mdd * 100}
