"""Screening acotado de Forex, futuros perpetuos y volatilidad de opciones (solo investigación).

Reglas, parámetros, costos y corte entre muestra y fuera de muestra FIJADOS
ANTES de ver resultados (PREREG). No se optimiza nada. Con varias pruebas
se aplica Bonferroni sobre el t-estadístico fuera de muestra.

Uso: python -m lab.research.screen salida.json
Datos públicos: FRED (tipos de cambio diarios), Binance USDⓈ-M (klines y
funding), Deribit (índice DVOL). Sin claves.
"""

import json
import math
import sys
from datetime import datetime, timezone

PREREG = {
    "fx": {"pairs": ["DEXUSEU", "DEXJPUS", "DEXUSUK", "DEXUSAL", "DEXCAUS", "DEXSZUS"],
           "rules": {"tsmom_20_100": "largo si media 20d > media 100d, corto si no",
                     "meanrev_5": "posición contraria al retorno de 5 días (z > 1: corto; z < -1: largo)",
                     "breakout_20": "largo al romper el máximo de 20d, corto al romper el mínimo; se mantiene"},
           "cost_per_turnover": 0.0002,      # 2 pb por cambio de posición unitario (spread + comisión, SUPUESTO)
           "swap_markup_yr": 0.02,           # 2%/año sobre el nominal mientras hay posición (SUPUESTO conservador)
           "split": "2015-12-31"},
    "perp": {"symbols": ["BTCUSDT", "ETHUSDT"],
             "rules": {"tsmom_20_100": "largo si media 20d > media 100d, corto si no",
                       "funding_carry": "corto perpetuo si el funding promedio de 7 días es > 0 (cobra funding), sin cobertura",
                       "funding_carry_hedged": "corto perpetuo + largo spot (neutral al precio) mientras el funding de 7 días sea > 0; "
                                               "agregado el 16/10 ANTES de ver su resultado: la versión sin cobertura era un error de "
                                               "especificación (es direccional, no carry)"},
             "hedged_cost_per_leg_change": 0.001 + 0.0005 + 0.0004,   # spot taker 0,10% + perp taker 0,05% (VERIFICADO) + 4 pb de deslizamiento (SUPUESTO)
             "hedged_capital_factor": 1.5,       # capital por USD de cobertura: 1 spot + 0,5 margen del perpetuo a 2x (SUPUESTO)
             "cost_per_turnover": 0.0005 + 0.0002,   # taker 0,05% (VERIFICADO, Binance USDⓈ-M) + 2 pb de deslizamiento (SUPUESTO)
             "split": "2023-12-31"},
    "vol": {"note": "prima de varianza: DVOL (IV 30d anualizada) contra la volatilidad realizada de los 30 días siguientes",
            "short_vol_cost_vol_pts": 2.0,     # costo de entrar y salir de opciones ATM: ~2 puntos de vol (SUPUESTO)
            "split": "2023-12-31"},
    "alpha": 0.05,
}


def _mean(x):
    return sum(x) / len(x) if x else float("nan")


def _std(x):
    m = _mean(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1)) if len(x) > 1 else float("nan")


def tstat(x):
    s = _std(x)
    return _mean(x) / (s / math.sqrt(len(x))) if x and s and s > 0 else 0.0


def positions(closes, rule):
    """Posición de cada día (decidida con datos HASTA ese cierre; se aplica al
    retorno del día siguiente: sin mirar el futuro)."""
    pos = []
    for i in range(len(closes)):
        p = 0.0
        if rule == "tsmom_20_100" and i >= 100:
            p = 1.0 if _mean(closes[i - 19:i + 1]) > _mean(closes[i - 99:i + 1]) else -1.0
        elif rule == "meanrev_5" and i >= 60:
            rets = [closes[k] / closes[k - 1] - 1 for k in range(i - 59, i + 1)]
            r5 = closes[i] / closes[i - 5] - 1
            z = r5 / (_std(rets) * math.sqrt(5)) if _std(rets) > 0 else 0
            p = -1.0 if z > 1 else (1.0 if z < -1 else 0.0)
        elif rule == "breakout_20" and i >= 20:
            hi, lo = max(closes[i - 20:i]), min(closes[i - 20:i])
            prev = pos[-1] if pos else 0.0
            p = 1.0 if closes[i] > hi else (-1.0 if closes[i] < lo else prev)
        pos.append(p)
    return pos


def backtest(dates, closes, pos, cost_turnover, carry_yr=0.0, funding=None):
    """Retornos netos diarios: pos[i-1] * ret[i] − costo por cambio de posición
    − markup de swap/financiación. funding[i]: tasa pagada por los largos ese día."""
    out = []
    for i in range(1, len(closes)):
        r = closes[i] / closes[i - 1] - 1
        p, prev = pos[i - 1], (pos[i - 2] if i >= 2 else 0.0)
        net = p * r - abs(p - prev) * cost_turnover - abs(p) * carry_yr / 252
        if funding is not None:
            net -= p * funding[i]
        out.append((dates[i], net))
    return out


def stats(rets):
    x = [r for _, r in rets]
    if not x:
        return {"n": 0}
    eq, peak, mdd = 1.0, 1.0, 0.0
    for r in x:
        eq *= 1 + r
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    return {"n": len(x), "total_return": eq - 1, "mean_daily": _mean(x), "t": tstat(x),
            "max_drawdown": mdd, "hit_rate": sum(r > 0 for r in x) / len(x)}


def split_stats(rets, split):
    ins = [(d, r) for d, r in rets if d <= split]
    oos = [(d, r) for d, r in rets if d > split]
    return {"in_sample": stats(ins), "out_of_sample": stats(oos)}


# ---------- datos ----------

def fred(series):
    import requests
    txt = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": series}, timeout=60).text
    d, c = [], []
    for line in txt.splitlines()[1:]:
        a, b = line.split(",")
        if b not in (".", ""):
            d.append(a)
            c.append(float(b))
    return d, c


def binance_daily(symbol):
    import requests
    out, start = [], 1567296000000          # 2019-09-01
    while True:
        k = requests.get("https://fapi.binance.com/fapi/v1/klines", timeout=60,
                         params={"symbol": symbol, "interval": "1d", "startTime": start, "limit": 1500}).json()
        if not k:
            break
        out += k
        start = k[-1][0] + 86_400_000
        if len(k) < 1500:
            break
    dates = [datetime.fromtimestamp(x[0] / 1000, timezone.utc).strftime("%Y-%m-%d") for x in out]
    return dates, [float(x[4]) for x in out]


def binance_funding_daily(symbol):
    import requests
    fr, start = {}, 1567296000000
    while True:
        rows = requests.get("https://fapi.binance.com/fapi/v1/fundingRate", timeout=60,
                            params={"symbol": symbol, "startTime": start, "limit": 1000}).json()
        if not rows:
            break
        for r in rows:
            d = datetime.fromtimestamp(r["fundingTime"] / 1000, timezone.utc).strftime("%Y-%m-%d")
            fr[d] = fr.get(d, 0.0) + float(r["fundingRate"])
        start = rows[-1]["fundingTime"] + 1
        if len(rows) < 1000:
            break
    return fr


def dvol(currency="BTC"):
    import requests
    out, end = {}, int(datetime.now(timezone.utc).timestamp() * 1000)
    start = 1617235200000                   # 2021-04-01 (inicio del DVOL)
    while end > start:
        r = requests.get("https://www.deribit.com/api/v2/public/get_volatility_index_data", timeout=60,
                         params={"currency": currency, "start_timestamp": start, "end_timestamp": end,
                                 "resolution": "1D"}).json()["result"]
        rows = r["data"]
        if not rows:
            break
        for t, o, h, l, c in rows:
            out[datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m-%d")] = c
        end = rows[0][0] - 1
        if len(rows) < 2:
            break
    return out


# ---------- pruebas ----------

def run_fx():
    P = PREREG["fx"]
    res = {}
    for s in P["pairs"]:
        d, c = fred(s)
        for rule in P["rules"]:
            pos = positions(c, rule)
            res[f"{s}:{rule}"] = split_stats(backtest(d, c, pos, P["cost_per_turnover"], P["swap_markup_yr"]),
                                             P["split"])
    return res


def run_perp():
    P = PREREG["perp"]
    res = {}
    for s in P["symbols"]:
        d, c = binance_daily(s)
        fr = binance_funding_daily(s)
        f = [fr.get(x, 0.0) for x in d]
        pos = positions(c, "tsmom_20_100")
        res[f"{s}:tsmom_20_100"] = split_stats(backtest(d, c, pos, P["cost_per_turnover"], funding=f), P["split"])
        fpos = []
        for i in range(len(d)):
            avg = _mean(f[max(0, i - 6):i + 1])
            fpos.append(-1.0 if i >= 7 and avg > 0 else 0.0)
        res[f"{s}:funding_carry"] = split_stats(backtest(d, c, fpos, P["cost_per_turnover"], funding=f), P["split"])
        # cubierto: el precio se cancela; queda el funding cobrado menos costos de abrir/cerrar
        # las dos patas, por unidad de CAPITAL (spot + margen)
        hedged = []
        for i in range(1, len(d)):
            on, prev = -fpos[i - 1], (-fpos[i - 2] if i >= 2 else 0.0)
            net = on * f[i] - abs(on - prev) * P["hedged_cost_per_leg_change"]
            hedged.append((d[i], net / P["hedged_capital_factor"]))
        res[f"{s}:funding_carry_hedged"] = split_stats(hedged, P["split"])
    return res


def run_vol():
    """Short de volatilidad a 30 días (aproximación de swap de varianza):
    P&L por punto de vol ≈ (IV − RV_30d_siguientes) − costo. Se informa
    también la cola: no es una estrategia de riesgo definido."""
    P = PREREG["vol"]
    iv = dvol("BTC")
    d, c = binance_daily("BTCUSDT")
    idx = {x: i for i, x in enumerate(d)}
    rows = []
    for day, v in sorted(iv.items()):
        i = idx.get(day)
        if i is None or i + 30 >= len(c):
            continue
        rets = [math.log(c[k] / c[k - 1]) for k in range(i + 1, i + 31)]
        rv = _std(rets) * math.sqrt(365) * 100
        rows.append((day, v - rv - P["short_vol_cost_vol_pts"], v, rv))
    ins = [r for r in rows if r[0] <= P["split"]]
    oos = [r for r in rows if r[0] > P["split"]]
    monthly = {"in_sample": [r[1] for r in ins[::30]], "out_of_sample": [r[1] for r in oos[::30]]}

    def s(x):
        e = sorted(r[1] for r in x)
        return {"n": len(e), "mean_edge_vol_pts": _mean(e), "median": e[len(e) // 2] if e else None,
                "worst": e[0] if e else None, "p5": e[int(0.05 * (len(e) - 1))] if e else None,
                "share_positive": sum(v > 0 for v in e) / len(e) if e else None,
                "mean_iv": _mean([r[2] for r in x]), "mean_rv": _mean([r[3] for r in x]),
                "note": "observaciones diarias solapadas a 30 días: t no válido (n efectivo ≈ n/30)"}
    return {"in_sample": {**s(ins), "monthly_nonoverlap_n": len(monthly["in_sample"]),
                          "monthly_nonoverlap_t": tstat(monthly["in_sample"])},
            "out_of_sample": {**s(oos), "monthly_nonoverlap_n": len(monthly["out_of_sample"]),
                              "monthly_nonoverlap_t": tstat(monthly["out_of_sample"])}}


def bonferroni(results, alpha):
    n = len(results)
    z_crit = {0.05: 1.96}.get(alpha, 1.96)
    # cota normal de Bonferroni: alpha/n a dos colas
    from statistics import NormalDist
    z_b = NormalDist().inv_cdf(1 - alpha / (2 * n)) if n else z_crit
    return {"tests": n, "t_crit_bonferroni": z_b,
            "pass": [k for k, v in results.items()
                     if v["out_of_sample"].get("t", 0) > z_b and v["in_sample"].get("t", 0) > 0]}


def main():
    out = {"prereg": PREREG, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    out["fx"] = run_fx()
    out["perp"] = run_perp()
    tests = {**out["fx"], **out["perp"]}
    out["bonferroni"] = bonferroni(tests, PREREG["alpha"])
    out["vol"] = run_vol()
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, default=str)
    for k, v in tests.items():
        i, o = v["in_sample"], v["out_of_sample"]
        print(f"{k:28s} IS {i['total_return']*100:+8.1f}% t {i['t']:+.2f} | OOS {o['total_return']*100:+7.1f}% "
              f"t {o['t']:+.2f} DD {o['max_drawdown']*100:6.1f}% n {o['n']}")
    print("Bonferroni:", out["bonferroni"])
    print("vol:", json.dumps(out["vol"], default=str))


if __name__ == "__main__":
    main()
