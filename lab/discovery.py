"""Motor de descubrimiento de hipótesis (estadísticas; nunca arbitraje).

Reglas que impiden fabricar ganadores:
  * CRITERIOS CONGELADOS en el código (CRITERIA) con su hash. Un test fija el
    hash: cambiarlos exige un cambio explícito y revisado, no un ajuste
    automático. El motor nunca modifica criterios ni umbrales.
  * Separación cronológica entrenamiento / validación / prueba (60/20/20). Los
    umbrales de cada hipótesis se calculan SOLO con entrenamiento.
  * Se registran TODAS las hipótesis probadas (también las que fracasan) y la
    corrección de Benjamini-Hochberg se aplica sobre TODAS, incluidas las que
    vienen de otros estudios (pares, desbalance).
  * Promoción solo si: BH en entrenamiento, media neta > 0 en validación y en
    prueba, n mínimo y neto de prueba > 0 con costos x1.5.
"""

import hashlib
import json
import math
import sqlite3
import time
from pathlib import Path
from typing import Callable, Dict, List

from .research.stats import bh_reject, mean, ttest_mean_gt0

CRITERIA = {
    "version": 1,
    "split": [0.6, 0.2, 0.2],
    "bh_q": 0.10,
    "min_train_trades": 30,
    "min_test_trades": 30,
    "validation_mean_gt0": True,
    "test_mean_gt0": True,
    "test_cost_stress": 1.5,
}
CRITERIA_HASH = hashlib.sha256(json.dumps(CRITERIA, sort_keys=True).encode()).hexdigest()

FEE = 0.0010          # ASSUMED: taker spot nivel base
PERP_FEE = 0.0005     # ASSUMED: taker perpetuo nivel base
SLIP = 0.0001         # ASSUMED: medio spread sobre cierres (no son precios ejecutables)


def _quantile(xs, q):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * (len(s) - 1)))] if s else 0.0


def splits(n):
    a, b, _ = CRITERIA["split"]
    i1, i2 = int(n * a), int(n * (a + b))
    return (0, i1), (i1, i2), (i2, n)


# ------------------------------------------------------------ familias -----

def momentum_hypotheses(asset, closes: List[float]):
    """ret_k > umbral (cuantil 0.8 de |ret_k| en ENTRENAMIENTO) -> posición en la
    dirección (momentum) o contraria (reversión) por h horas, sin solapamiento."""
    n = len(closes)
    (tr0, tr1), _, _ = splits(n)
    out = []
    for k in (1, 4, 24):
        rets = [math.log(closes[t] / closes[t - k]) for t in range(max(k, tr0), tr1)]
        thr = _quantile([abs(r) for r in rets], 0.8)
        for h in (1, 4, 24):
            for mode in ("momentum", "reversal"):
                def trades(lo, hi, k=k, h=h, mode=mode, thr=thr):
                    tr, t = [], max(lo, k)
                    while t + h < hi:
                        r = math.log(closes[t] / closes[t - k])
                        if abs(r) > thr:
                            d = (1 if r > 0 else -1) * (1 if mode == "momentum" else -1)
                            g = d * math.log(closes[t + h] / closes[t])
                            tr.append({"t": t, "gross": g, "cost": 2 * (FEE + SLIP)})
                            t += h
                        else:
                            t += 1
                    return tr
                out.append({"id": f"mom|{asset}|k{k}|h{h}|{mode}", "family": "precio_momentum",
                            "params": {"asset": asset, "k": k, "h": h, "mode": mode,
                                       "threshold_from_train": thr},
                            "n": n, "trades_fn": trades})
    return out


def funding_hypotheses(name, perp_closes: List[float], funding_by_index: Dict[int, float]):
    """Funding en cuantiles extremos (de ENTRENAMIENTO) -> posición en el perpetuo
    a favor o en contra del lado pagador, por h horas; incluye el funding cobrado."""
    n = len(perp_closes)
    (tr0, tr1), _, _ = splits(n)
    train_rates = [r for i, r in funding_by_index.items() if tr0 <= i < tr1]
    if len(train_rates) < 20:
        return []
    hi_q, lo_q = _quantile(train_rates, 0.9), _quantile(train_rates, 0.1)
    out = []
    for h in (8, 24):
        for mode in ("contrarian", "continuation"):
            def trades(lo, hi, h=h, mode=mode):
                tr, idx = [], sorted(i for i in funding_by_index if lo <= i < hi - h)
                last = -10**9
                for i in idx:
                    if i < last + h:
                        continue
                    r = funding_by_index[i]
                    if r > hi_q:
                        d = -1 if mode == "contrarian" else 1
                    elif r < lo_q:
                        d = 1 if mode == "contrarian" else -1
                    else:
                        continue
                    g = d * math.log(perp_closes[i + h] / perp_closes[i])
                    fund = sum(-d * funding_by_index[j] for j in funding_by_index if i < j <= i + h)
                    tr.append({"t": i, "gross": g + fund, "cost": 2 * (PERP_FEE + SLIP)})
                    last = i
                return tr
            out.append({"id": f"fund|{name}|h{h}|{mode}", "family": "funding_extremo",
                        "params": {"market": name, "h": h, "mode": mode,
                                   "q90_train": hi_q, "q10_train": lo_q},
                        "n": n, "trades_fn": trades})
    return out


# ------------------------------------------------------------ evaluación ---

def evaluate_hypothesis(h):
    (a0, a1), (v0, v1), (t0, t1) = splits(h["n"])
    tr, va, te = h["trades_fn"](a0, a1), h["trades_fn"](v0, v1), h["trades_fn"](t0, t1)
    nets = lambda xs, s=1.0: [x["gross"] - s * x["cost"] for x in xs]  # noqa: E731
    t, p = ttest_mean_gt0(nets(tr))
    return {"id": h["id"], "family": h["family"], "params": h["params"], "p_train": p,
            "t_train": t, "n_train": len(tr), "train_net_mean": mean(nets(tr)) if tr else None,
            "train_gross_mean": mean([x["gross"] for x in tr]) if tr else None,
            "n_val": len(va), "val_net_mean": mean(nets(va)) if va else None,
            "n_test": len(te), "test_net_mean": mean(nets(te)) if te else None,
            "test_net_sum": sum(nets(te)),
            "test_net_sum_stress": sum(nets(te, CRITERIA["test_cost_stress"]))}


def external_hypothesis(hid, family, p_train, n_train, n_test, test_net_sum, test_stress_sum,
                        params=None):
    """Hipótesis de otro estudio (pares, desbalance) para la corrección GLOBAL."""
    return {"id": hid, "family": family, "params": params or {}, "p_train": p_train,
            "n_train": n_train, "n_val": None, "val_net_mean": None, "n_test": n_test,
            "test_net_mean": (test_net_sum / n_test) if n_test else None,
            "test_net_sum": test_net_sum, "test_net_sum_stress": test_stress_sum,
            "external": True}


def decide(results):
    """BH global + criterios congelados. Modifica y devuelve results."""
    rej = bh_reject([r["p_train"] for r in results], CRITERIA["bh_q"]) if results else []
    for r, bh in zip(results, rej):
        r["bh_train"] = bh
        stages = {
            "bh_train": bh,
            "min_train": (r["n_train"] or 0) >= CRITERIA["min_train_trades"],
            "validation": r.get("external") or ((r["val_net_mean"] or 0) > 0),
            "min_test": (r["n_test"] or 0) >= CRITERIA["min_test_trades"],
            "test_mean": (r["test_net_mean"] or 0) > 0,
            "test_stress": (r["test_net_sum_stress"] or 0) > 0,
        }
        r["stages"] = stages
        r["promoted"] = all(stages.values())
        r["failed_at"] = next((k for k, v in stages.items() if not v), None)
    return results


class Registry:
    """Registro persistente de TODAS las hipótesis probadas."""

    def __init__(self, path=Path("lab_data") / "discovery.sqlite"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS tests (run TEXT, at REAL, criteria_hash TEXT, "
                        "id TEXT, family TEXT, promoted INTEGER, failed_at TEXT, data TEXT)")

    def record(self, run, results):
        self.db.executemany("INSERT INTO tests VALUES (?,?,?,?,?,?,?,?)", [
            (run, time.time(), CRITERIA_HASH, r["id"], r["family"], int(r["promoted"]),
             r["failed_at"], json.dumps(r, default=str)) for r in results])
        self.db.commit()

    def count(self, run=None):
        q = "SELECT COUNT(*) FROM tests" + (" WHERE run=?" if run else "")
        return self.db.execute(q, (run,) if run else ()).fetchone()[0]


def run_discovery(hypotheses, externals=(), registry=None, run_id=None):
    results = [evaluate_hypothesis(h) for h in hypotheses] + list(externals)
    decide(results)
    run_id = run_id or time.strftime("disc-%Y%m%dT%H%M%S")
    if registry is not None:
        registry.record(run_id, results)
    funnel = {"tested": len(results),
              "bh_train": sum(r["bh_train"] for r in results),
              "passed_validation": sum(r["bh_train"] and r["stages"]["validation"] for r in results),
              "promoted": sum(r["promoted"] for r in results)}
    return {"run": run_id, "criteria": CRITERIA, "criteria_hash": CRITERIA_HASH,
            "funnel": funnel, "by_family": _by_family(results), "results": results}


def _by_family(results):
    fam = {}
    for r in results:
        d = fam.setdefault(r["family"], {"tested": 0, "bh_train": 0, "promoted": 0})
        d["tested"] += 1
        d["bh_train"] += r["bh_train"]
        d["promoted"] += r["promoted"]
    return fam
