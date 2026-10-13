"""I — Microestructura: ¿el desbalance del libro predice el próximo movimiento?

Datos: snapshots guardados del laboratorio (mismo libro T0 que vieron los
módulos). Para cada (venue, símbolo) y par de ticks consecutivos:
  desbalance = (vol_bid - vol_ask) / (vol_bid + vol_ask) en los 5 primeros niveles
  regla(θ): si desbalance > θ compra al ask y vende al bid del tick siguiente;
            si < -θ, lo opuesto (requiere poder vender en corto: ASSUMED via margen).
Costos: se cruza el spread dos veces (precios ejecutables) + 2 comisiones taker.
Separación cronológica 70/30; BH sobre TODAS las combinaciones (venue,
símbolo, θ). Siempre ESTADISTICA, nunca garantizado.
"""

from collections import defaultdict
from dataclasses import asdict, dataclass

from .stats import bh_reject, mean, ttest_mean_gt0

THRESHOLDS = (0.3, 0.5, 0.7)


@dataclass(frozen=True)
class ImbalanceConfig:
    levels: int = 5
    fee: float = 0.0010          # ASSUMED: taker de nivel base
    test_fraction: float = 0.30
    min_trades: int = 20
    bh_q: float = 0.10


def imbalance(book, levels=5):
    b = sum(q for _, q in book["bids"][:levels])
    a = sum(q for _, q in book["asks"][:levels])
    return (b - a) / (b + a) if (a + b) else 0.0


def collect_series(snapshots):
    """-> {(venue, símbolo): [(tick, ts, desbalance, best_bid, best_ask)]} sin guardar
    los libros completos en memoria."""
    out = defaultdict(list)
    for s in snapshots:
        for k, b in s.books.items():
            if b.get("bids") and b.get("asks"):
                v, sym = k.split("|")
                out[(v, sym)].append((s.tick, s.ts, imbalance(b), b["bids"][0][0], b["asks"][0][0]))
    return out


def trades_for(series, theta, fee):
    tr = []
    for (t0, ts0, imb, bid0, ask0), (t1, _, _, bid1, ask1) in zip(series, series[1:]):
        if t1 != t0 + 1:
            continue                      # solo ticks consecutivos
        if imb > theta:
            r = (bid1 - ask0) / ask0      # compra al ask, vende al bid siguiente
        elif imb < -theta:
            r = (bid0 - ask1) / bid0      # vende al bid, recompra al ask siguiente
        else:
            continue
        tr.append({"tick": t0, "ts": ts0, "gross": r, "net": r - 2 * fee})
    return tr


def evaluate(series_by_market, cfg: ImbalanceConfig = ImbalanceConfig()):
    hyps = []
    for (v, sym), ser in sorted(series_by_market.items()):
        ser = sorted(ser)
        split = int(len(ser) * (1 - cfg.test_fraction))
        for th in THRESHOLDS:
            train = trades_for(ser[:split], th, cfg.fee)
            test = trades_for(ser[split:], th, cfg.fee)
            t, p = ttest_mean_gt0([x["net"] for x in train])
            hyps.append({"market": f"{v}|{sym}", "theta": th, "train_trades": len(train),
                         "train_net_mean": mean([x["net"] for x in train]) if train else None,
                         "train_gross_mean": mean([x["gross"] for x in train]) if train else None,
                         "p": p, "test_trades": len(test),
                         "test_net_mean": mean([x["net"] for x in test]) if test else None})
    rej = bh_reject([h["p"] for h in hyps], cfg.bh_q) if hyps else []
    for h, r in zip(hyps, rej):
        h["bh_significant"] = r
        ok = (r and h["train_trades"] >= cfg.min_trades and h["test_trades"] >= cfg.min_trades
              and (h["test_net_mean"] or 0) > 0)
        h["verdict"] = "ESTADISTICA" if ok else ("SIN_EVIDENCIA" if r else "SIN_EDGE")
    return {"config": asdict(cfg), "hypotheses_tested": len(hyps), "bh_rejections": sum(rej),
            "results": hyps}
