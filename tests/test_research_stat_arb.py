import math
import random

import pytest

from lab.research.stat_arb import StatArbConfig, align, evaluate_pairs, trade_window


def synthetic(n=3000, seed=3, coint=True):
    """x paseo aleatorio; y = x + ruido AR(0.9) si cointegran, o paseo propio si no."""
    rng = random.Random(seed)
    x, y, z, ny = [0.0], [0.0], [0.0], 0.0
    for _ in range(n - 1):
        x.append(x[-1] + rng.gauss(0, 0.01))
        ny = 0.9 * ny + rng.gauss(0, 0.004)
        y.append(x[-1] + ny if coint else y[-1] + rng.gauss(0, 0.01))
        z.append(z[-1] + rng.gauss(0, 0.01))
    return {"Y": y, "X": x, "Z": z}


def test_align_uses_only_common_timestamps():
    ts, s = align({"A": {1: 1.0, 2: math.e, 3: 1.0}, "B": {2: 1.0, 3: 1.0}})
    assert ts == [2, 3] and s["A"] == [1.0, 0.0]


def test_trade_window_costs_four_executions_and_borrow():
    cfg = StatArbConfig(fee=0.001, slippage=0.0, borrow_per_hour=0.0)
    ly = [0.0, 0.03, 0.0]          # z sube a +3 y vuelve: short spread y cierre
    (t,) = trade_window(ly, [0.0, 0.0, 0.0], beta=1.0, mu=0.0, sd=0.01, cfg=cfg)
    assert t["gross"] == pytest.approx(0.03 / 2)
    assert t["cost"] == pytest.approx(0.002)          # 2 x (fee) por pata-lado en notional 1+|b|


def test_cointegrated_pair_found_without_costs_and_independent_ones_rejected():
    s = synthetic()
    cfg = StatArbConfig(fee=0.0, slippage=0.0, borrow_per_hour=0.0, min_trades=5)
    r = evaluate_pairs(s, len(s["X"]), cfg)
    res = {x["pair"]: x for x in r["results"]}
    assert res["X~Y"]["coint_window_share"] > 0.5
    assert res["X~Y"]["bh_significant"] and res["X~Y"]["oos"]["net_sum"] > 0
    assert not res["X~Z"]["bh_significant"]            # paseos independientes
    assert r["pairs_tested"] == 3                      # BH sobre TODOS los pares


def test_realistic_costs_kill_a_small_edge():
    s = synthetic()
    r = evaluate_pairs(s, len(s["X"]), StatArbConfig(fee=0.01, min_trades=5))   # 1% por ejecución
    assert all(x["verdict"] != "ESTADISTICA" for x in r["results"])


def test_out_of_sample_is_never_used_for_selection():
    s = synthetic()
    n = len(s["X"])
    cfg = StatArbConfig(fee=0.0, slippage=0.0, borrow_per_hour=0.0, min_trades=5)
    base = evaluate_pairs(s, n, cfg)
    # Arruinar SOLO el tramo fuera de muestra no cambia qué pares se seleccionan.
    broken = {k: v[:] for k, v in s.items()}
    split = base["split_index"]
    rng = random.Random(9)
    for i in range(split, n):
        broken["Y"][i] = broken["Y"][i - 1] + rng.gauss(0, 0.05)
    other = evaluate_pairs(broken, n, cfg)
    sel = lambda r: {x["pair"]: x["selected"] for x in r["results"]}  # noqa: E731
    assert sel(base) == sel(other)
