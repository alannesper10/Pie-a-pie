"""G — ETF equivalentes y ADR vs acción local (siempre ESTADISTICA; ejecución
NO_VERIFICABLE).

Relaciones económicas investigadas:
  * ETF que replican el MISMO índice/activo: SPY/IVV/VOO (S&P 500),
    QQQ/QQQM (Nasdaq-100), GLD/IAU (oro). Tienen distinto NAV por cuota, así
    que se estudia el log-cociente (beta fijo = 1: la relación es económica,
    no estimada), cuya deriva esperada es la diferencia de gastos.
  * ADR vs acción local (BYMA): CCL implícito = precio local x ratio / ADR.
    Se comparan CCL entre emisoras. Los ratios ADR se toman como SUPUESTOS y se
    VERIFICAN con los datos: si un CCL se aparta > 25% de la mediana del grupo,
    la relación queda RATIO_NO_VERIFICADO y se excluye (no se "corrige" a ojo).

Limitaciones que impiden clasificar como arbitraje: cierres diarios (no son
precios ejecutables ni simultáneos), sin bid/ask, horarios distintos,
restricciones de venta en corto, y en Argentina normas cambiarias del CCL.
"""

import math
from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Dict, List

from .stats import adf_tstat, bh_reject, eg_critical, mean, std, ttest_mean_gt0

ETF_GROUPS = {"S&P 500": ("SPY", "IVV", "VOO"), "Nasdaq-100": ("QQQ", "QQQM"),
              "Oro": ("GLD", "IAU")}
# ADR -> (acción local en BYMA, acciones por ADR). SUPUESTO: se verifica con datos.
ADR_RATIOS = {"GGAL": ("GGAL.BA", 10), "BMA": ("BMA.BA", 10), "PAM": ("PAMP.BA", 25),
              "YPF": ("YPFD.BA", 1)}
RATIO_TOLERANCE = 0.25


@dataclass(frozen=True)
class RelationConfig:
    formation_d: int = 120
    trading_d: int = 20
    entry_z: float = 2.0
    exit_z: float = 0.5
    cost_per_execution: float = 0.0002   # ASSUMED: comisión + medio spread (ETF líquidos)
    borrow_per_day: float = 0.003 / 365  # ASSUMED: préstamo de la pata corta
    test_fraction: float = 0.30
    min_trades: int = 8
    bh_q: float = 0.10


def relation_trades(spread: List[float], start, end, cfg: RelationConfig):
    """Walk-forward sobre un spread con beta fijo = 1 (relación económica)."""
    trades, windows = [], []
    w0 = start + cfg.formation_d
    while w0 + 2 <= end:
        form = spread[w0 - cfg.formation_d:w0]
        mu, sd = mean(form), std(form)
        tau = adf_tstat(form)
        windows.append({"start": w0, "tau": tau,
                        "stationary": tau is not None and tau < eg_critical(len(form))})
        w1 = min(w0 + cfg.trading_d, end)
        pos = 0
        for i in range(w0, w1):
            z = (spread[i] - mu) / sd if sd else 0.0
            last = i == w1 - 1
            if pos == 0 and not last and abs(z) > cfg.entry_z:
                pos, ei = (-1 if z > 0 else 1), i
            elif pos and (abs(z) < cfg.exit_z or last):
                gross = pos * (spread[i] - spread[ei]) / 2
                cost = 2 * cfg.cost_per_execution + cfg.borrow_per_day * (i - ei) / 2
                trades.append({"t_entry": ei, "t_exit": i, "gross": gross, "cost": cost,
                               "net": gross - cost})
                pos = 0
        w0 += cfg.trading_d
    return trades, windows


def ccl_series(closes: Dict[str, Dict[int, float]], ratios=ADR_RATIOS):
    """CCL implícito por emisora y verificación del ratio contra la mediana."""
    ccl, checks = {}, {}
    for adr, (local, ratio) in ratios.items():
        a, l = closes.get(adr), closes.get(local)
        if not a or not l:
            checks[adr] = "SIN_DATOS"
            continue
        common = sorted(set(a) & set(l))
        ccl[adr] = {t: l[t] * ratio / a[t] for t in common if a[t]}
    if len(ccl) >= 2:
        last = {k: v[max(v)] for k, v in ccl.items() if v}
        med = sorted(last.values())[len(last) // 2]
        for k, v in last.items():
            if abs(v / med - 1) > RATIO_TOLERANCE:
                checks[k] = f"RATIO_NO_VERIFICADO (CCL {v:.1f} vs mediana {med:.1f})"
                del ccl[k]
            else:
                checks[k] = f"OK (CCL {v:.1f})"
    return ccl, checks


def evaluate_relations(named_series: Dict[str, Dict[int, float]], pairs, cfg=RelationConfig(),
                       kind="ETF"):
    """named_series: {nombre: {ts: precio}}; pairs: [(a, b)]. Log-cociente a/b."""
    results, disc = [], []
    for a, b in pairs:
        if a not in named_series or b not in named_series:
            results.append({"pair": f"{a}~{b}", "kind": kind, "verdict": "SIN_DATOS"})
            continue
        common = sorted(set(named_series[a]) & set(named_series[b]))
        spread = [math.log(named_series[a][t] / named_series[b][t]) for t in common]
        n = len(spread)
        split = int(n * (1 - cfg.test_fraction))
        tr, win = relation_trades(spread, 0, split, cfg)
        t, p = ttest_mean_gt0([x["net"] for x in tr])
        disc.append((len(results), p))
        results.append({"pair": f"{a}~{b}", "kind": kind, "observations": n, "split": split,
                        "discovery_trades": len(tr), "discovery_net_sum": sum(x["net"] for x in tr),
                        "discovery_gross_sum": sum(x["gross"] for x in tr), "p": p, "t": t,
                        "stationary_window_share": (sum(w["stationary"] for w in win) / len(win))
                        if win else 0.0, "_spread": spread})
    rej = bh_reject([p for _, p in disc], cfg.bh_q) if disc else []
    for (idx, _), r in zip(disc, rej):
        res = results[idx]
        spread = res.pop("_spread")
        res["bh_significant"] = r
        res["selected"] = r and res["discovery_trades"] >= cfg.min_trades
        res["oos"] = None
        if res["selected"]:
            tr, _ = relation_trades(spread, res["split"] - cfg.formation_d, len(spread), cfg)
            tr = [x for x in tr if x["t_entry"] >= res["split"]]
            res["oos"] = {"trades": len(tr), "net_sum": sum(x["net"] for x in tr),
                          "net_sum_costs_x1.5": sum(x["gross"] - 1.5 * x["cost"] for x in tr)}
        ok = (res["selected"] and res["oos"] and res["oos"]["trades"] >= cfg.min_trades
              and res["oos"]["net_sum"] > 0 and res["oos"]["net_sum_costs_x1.5"] > 0)
        res["verdict"] = "ESTADISTICA" if ok else ("SIN_EVIDENCIA" if res["selected"] else "SIN_EDGE")
        res["execution"] = "NO_VERIFICABLE (cierres diarios, sin bid/ask ni simultaneidad)"
    for res in results:
        res.pop("_spread", None)
    return {"config": asdict(cfg), "pairs_tested": len(disc), "bh_rejections": sum(rej),
            "results": results}


def etf_pairs():
    return [p for g in ETF_GROUPS.values() for p in combinations(g, 2)]
