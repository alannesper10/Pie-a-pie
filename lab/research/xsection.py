"""E1 y E2 (BIBLIOTECA_INTEGRADA_2026-10-16.md, reglas registradas en ea6e551).

E1  momentum entre activos (hipótesis propia sobre Chan Ej. 6.2): cada 7 días,
    rankear por retorno de 30 días; largo top 4 / corto bottom 4, 0,125 cada uno.
E2  reversión lineal entre activos (Chan Ej. 4.3): w_i = −(r_i − r̄)/Σ|r_j − r̄|
    con el retorno del día anterior; rebalanceo diario.
Retorno diario = Σ w_{t−1}·r_t − Σ w_{t−1}·funding_t − rotación·costo.
El funding lo pagan los largos y lo cobran los cortos (signo de Binance).
Solo se usan monedas con dato ese día (nada se rellena).
"""

import math

COST = 0.0005 + 0.0002          # taker 0,05% (VERIFICADO) + 2 pb (SUPUESTO)
MAKER_COST = 0.0002 + 0.0002    # escenario maker (informativo, Harris cap. 18)
TOP = 4
LOOKBACK = 30
HOLD = 7


def momentum_weights(closes, day_idx, days):
    """Pesos al cierre de days[day_idx] con datos hasta ese día."""
    if day_idx < LOOKBACK:
        return {}
    d, d0 = days[day_idx], days[day_idx - LOOKBACK]
    rets = {s: c[d] / c[d0] - 1 for s, c in closes.items() if d in c and d0 in c}
    if len(rets) < 2 * TOP:
        return {}
    order = sorted(rets, key=rets.get)
    w = {s: -1 / (2 * TOP) for s in order[:TOP]}
    w.update({s: 1 / (2 * TOP) for s in order[-TOP:]})
    return w


def reversal_weights(closes, day_idx, days):
    if day_idx < 1:
        return {}
    d, d0 = days[day_idx], days[day_idx - 1]
    rets = {s: c[d] / c[d0] - 1 for s, c in closes.items() if d in c and d0 in c}
    if len(rets) < 4:
        return {}
    m = sum(rets.values()) / len(rets)
    dev = {s: -(r - m) for s, r in rets.items()}
    tot = sum(abs(v) for v in dev.values())
    return {s: v / tot for s, v in dev.items()} if tot > 0 else {}


def run(closes, funding, days, strategy, cost=COST):
    """-> lista de (día, retorno neto). closes/funding: {símbolo: {día: valor}}."""
    out, w, last_rebal = [], {}, None
    for i in range(1, len(days)):
        d, p = days[i], days[i - 1]
        r = 0.0
        for s, wt in w.items():
            c = closes[s]
            if d in c and p in c:
                r += wt * (c[d] / c[p] - 1) - wt * funding.get(s, {}).get(d, 0.0)
        if strategy == "momentum":
            new = momentum_weights(closes, i, days) if (last_rebal is None or i - last_rebal >= HOLD) else w
            if new is not w:
                last_rebal = i
        else:
            new = reversal_weights(closes, i, days)
        turnover = sum(abs(new.get(s, 0) - w.get(s, 0)) for s in set(new) | set(w))
        r -= turnover * cost
        w = new
        out.append((d, r))
    return out


def stats(rets, block=7):
    x = [r for _, r in rets]
    blocks = [sum(x[i:i + block]) for i in range(0, len(x) - block + 1, block)]
    n = len(blocks)
    if n < 2:
        return {"n": n}
    m = sum(blocks) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in blocks) / (n - 1))
    eq, peak, mdd = 1.0, 1.0, 0.0
    for v in x:
        eq *= 1 + v
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    yrs = len(x) / 365
    return {"blocks": n, "t": m / (sd / math.sqrt(n)) if sd > 0 else None, "total_pct": (eq - 1) * 100,
            "ann_pct": (eq ** (1 / yrs) - 1) * 100 if yrs > 0 and eq > 0 else None,
            "max_drawdown_pct": mdd * 100, "days": len(x)}


UNIVERSE = ["BTC", "ETH", "BNB", "XRP", "ADA", "DOGE", "DOT", "LTC", "LINK", "BCH", "XLM", "UNI", "SOL",
            "AVAX", "ATOM", "ETC", "FIL", "TRX", "EOS", "AAVE"]


def fetch(s, start_ms=1609459200000):
    """Velas diarias y funding diario (suma) de los perpetuos USDT de Binance del universo."""
    from datetime import datetime, timezone

    def d(ms):
        return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")
    closes, funding, missing = {}, {}, []
    for coin in UNIVERSE:
        sym = coin + "USDT"
        c, t = {}, start_ms
        while True:
            rows = s.get("https://fapi.binance.com/fapi/v1/klines", timeout=60,
                         params={"symbol": sym, "interval": "1d", "startTime": t, "limit": 1500}).json()
            if not isinstance(rows, list) or not rows:
                break
            for r in rows:
                c[d(r[0])] = float(r[4])
            t = rows[-1][0] + 86_400_000
            if len(rows) < 1500:
                break
        if not c:
            missing.append(sym)
            continue
        f, t = {}, start_ms
        while True:
            rows = s.get("https://fapi.binance.com/fapi/v1/fundingRate", timeout=60,
                         params={"symbol": sym, "startTime": t, "limit": 1000}).json()
            if not isinstance(rows, list) or not rows:
                break
            for r in rows:
                k = d(r["fundingTime"])
                f[k] = f.get(k, 0.0) + float(r["fundingRate"])
            t = rows[-1]["fundingTime"] + 1
            if len(rows) < 1000:
                break
        closes[sym], funding[sym] = c, f
    return closes, funding, missing
