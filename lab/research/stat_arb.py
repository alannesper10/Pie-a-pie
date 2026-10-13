"""H — Arbitraje estadístico de pares (siempre ESTADISTICA, nunca garantizado).

Procedimiento (sin información futura):
  1. Serie horaria alineada; el 30% final queda RESERVADO como fuera de muestra.
  2. Walk-forward en el período de descubrimiento: en cada ventana de formación
     (30 d) se estima beta por OLS y se testea cointegración (ADF de Engle-
     Granger vs crítico de MacKinnon al 5%). Solo si pasa, se opera la ventana
     siguiente (7 d) con z = (spread - media) / desvío de la FORMACIÓN.
  3. Costos por operación: 4 ejecuciones (abrir/cerrar 2 patas) x (comisión +
     deslizamiento) + costo de préstamo/funding de la pata corta por hora.
  4. Test t de una cola por par y Benjamini-Hochberg sobre TODOS los pares.
  5. Solo los pares que sobreviven BH se evalúan en el fuera de muestra, con
     el MISMO procedimiento y parámetros. No se reajusta nada con esos datos.
  6. Régimen: fracción de ventanas cointegradas y deriva de beta.
"""

import math
from dataclasses import asdict, dataclass, field
from itertools import combinations
from typing import Dict, List

from .stats import adf_tstat, bh_reject, eg_critical, half_life, mean, ols, std, ttest_mean_gt0


@dataclass(frozen=True)
class StatArbConfig:
    formation_h: int = 720
    trading_h: int = 168
    entry_z: float = 2.0
    exit_z: float = 0.5
    fee: float = 0.0010            # ASSUMED: taker de nivel base por ejecución
    slippage: float = 0.0002       # ASSUMED: por ejecución
    borrow_per_hour: float = 0.0001 / 8   # ASSUMED: préstamo/funding de la pata corta
    test_fraction: float = 0.30
    min_trades: int = 10
    bh_q: float = 0.10


def align(closes: Dict[str, Dict[int, float]]):
    """-> (timestamps comunes, {símbolo: [log precio]})."""
    common = sorted(set.intersection(*(set(c) for c in closes.values()))) if closes else []
    return common, {s: [math.log(c[t]) for t in common] for s, c in closes.items()}


def trade_window(ly, lx, beta, mu, sd, cfg: StatArbConfig, t0=0):
    """Opera una ventana con parámetros FIJADOS en la formación."""
    trades, pos, entry_i, entry_s = [], 0, None, None
    weight = 1 + abs(beta)
    for i in range(len(ly)):
        s = ly[i] - beta * lx[i]
        z = (s - mu) / sd if sd else 0.0
        last = i == len(ly) - 1
        if pos == 0 and not last and abs(z) > cfg.entry_z:
            pos, entry_i, entry_s = (-1 if z > 0 else 1), i, s
        elif pos != 0 and (abs(z) < cfg.exit_z or last):
            gross = pos * (s - entry_s) / weight
            hours = i - entry_i
            cost = 2 * (cfg.fee + cfg.slippage) + cfg.borrow_per_hour * hours * (
                (abs(beta) if pos > 0 else 1) / weight)
            trades.append({"t_entry": t0 + entry_i, "t_exit": t0 + i, "hours": hours,
                           "gross": gross, "cost": cost, "net": gross - cost})
            pos = 0
    return trades


def walk_forward(ly, lx, start, end, cfg: StatArbConfig):
    trades, windows = [], []
    w0 = start + cfg.formation_h
    while w0 + 24 <= end:
        f_y, f_x = ly[w0 - cfg.formation_h:w0], lx[w0 - cfg.formation_h:w0]
        a, b, res = ols(f_x, f_y)
        tau = adf_tstat(res)
        coint = tau is not None and tau < eg_critical(len(res))
        windows.append({"start": w0, "beta": b, "tau": tau, "coint": coint,
                        "half_life_h": half_life(res)})
        if coint:
            w1 = min(w0 + cfg.trading_h, end)
            trades += trade_window(ly[w0:w1], lx[w0:w1], b, mean(res) + a, std(res), cfg, t0=w0)
        w0 += cfg.trading_h
    return trades, windows


def evaluate_pairs(series: Dict[str, List[float]], n: int, cfg: StatArbConfig = StatArbConfig()):
    split = int(n * (1 - cfg.test_fraction))
    pairs = list(combinations(sorted(series), 2))
    disc = {}
    for y, x in pairs:
        tr, win = walk_forward(series[y], series[x], 0, split, cfg)
        t, p = ttest_mean_gt0([r["net"] for r in tr])
        disc[(y, x)] = {"trades": tr, "windows": win, "t": t, "p": p}
    keys = list(disc)
    rejected = bh_reject([disc[k]["p"] for k in keys], cfg.bh_q) if keys else []
    out = []
    for k, rej in zip(keys, rejected):
        d = disc[k]
        nets = [r["net"] for r in d["trades"]]
        betas = [w["beta"] for w in d["windows"]]
        selected = rej and len(nets) >= cfg.min_trades
        oos = None
        if selected:   # mismo procedimiento sobre el período reservado
            tr, win = walk_forward(series[k[0]], series[k[1]], split - cfg.formation_h, n, cfg)
            tr = [r for r in tr if r["t_entry"] >= split]
            o_nets = [r["net"] for r in tr]
            oos = {"trades": len(o_nets), "net_sum": sum(o_nets),
                   "net_mean": mean(o_nets) if o_nets else None,
                   "gross_sum": sum(r["gross"] for r in tr),
                   "cost_sum": sum(r["cost"] for r in tr),
                   "net_sum_costs_x1.5": sum(r["gross"] - 1.5 * r["cost"] for r in tr)}
        verdict = ("ESTADISTICA" if selected and oos and oos["trades"] >= cfg.min_trades
                   and oos["net_sum"] > 0 and oos["net_sum_costs_x1.5"] > 0 else
                   "SIN_EVIDENCIA" if selected else "SIN_EDGE")
        out.append({
            "pair": f"{k[0]}~{k[1]}", "discovery_trades": len(nets),
            "discovery_net_sum": sum(nets), "discovery_gross_sum": sum(r["gross"] for r in d["trades"]),
            "discovery_cost_sum": sum(r["cost"] for r in d["trades"]),
            "t": d["t"], "p": d["p"], "bh_significant": rej, "selected": selected,
            "coint_window_share": (sum(w["coint"] for w in d["windows"]) / len(d["windows"])
                                   if d["windows"] else 0.0),
            "beta_drift_std": std(betas) if len(betas) > 1 else None,
            "oos": oos, "verdict": verdict})
    return {"config": asdict(cfg), "observations": n, "split_index": split,
            "pairs_tested": len(pairs), "bh_rejections": sum(rejected), "results": out}


def load_universe(history, exchange, symbols, days, now_ms, tf="1h"):
    """Cierres horarios desde la caché incremental (descarga solo lo que falta)."""
    from ..history import ccxt_fetcher
    since = now_ms - days * 86_400_000
    closes, errors = {}, []
    for s in symbols:
        r = history.ensure(exchange.id, s, tf, since, now_ms, ccxt_fetcher(exchange, s, tf))
        errors += r["errors"]
        c = history.closes(exchange.id, s, tf, since, now_ms)
        if c:
            closes[s] = c
    return closes, errors
