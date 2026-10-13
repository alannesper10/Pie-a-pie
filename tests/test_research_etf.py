import math
import random

import pytest

from lab.research.etf import RelationConfig, ccl_series, etf_pairs, evaluate_relations

D = 86_400_000


def test_ccl_ratio_is_verified_against_data_not_guessed():
    closes = {"GGAL": {1: 37.0, 2: 37.2}, "GGAL.BA": {1: 5950.0, 2: 5980.0},
              "BMA": {1: 65.8, 2: 65.8}, "BMA.BA": {1: 10600.0, 2: 10610.0},
              "YPF": {1: 52.1, 2: 52.1}, "YPFD.BA": {1: 8400.0, 2: 8400.0}}
    ccl, checks = ccl_series(closes, {"GGAL": ("GGAL.BA", 10), "BMA": ("BMA.BA", 10),
                                      "YPF": ("YPFD.BA", 1)})
    assert set(ccl) == {"GGAL", "BMA"}
    assert checks["YPF"].startswith("RATIO_NO_VERIFICADO")
    assert ccl["GGAL"][2] == pytest.approx(5980 * 10 / 37.2)


def test_missing_series_are_reported():
    ccl, checks = ccl_series({"GGAL": {1: 1.0}}, {"GGAL": ("GGAL.BA", 10)})
    assert ccl == {} and checks["GGAL"] == "SIN_DATOS"


def _pair(n=700, seed=4, kappa=0.3, noise=0.004):
    rng = random.Random(seed)
    a, b, d = {}, {}, 0.0
    level = 100.0
    for t in range(n):
        level *= math.exp(rng.gauss(0, 0.01))
        d = (1 - kappa) * d + rng.gauss(0, noise)
        a[t * D], b[t * D] = level * math.exp(d), level / 2
    return a, b


def test_mean_reverting_relation_without_costs_vs_with_realistic_costs():
    a, b = _pair()
    free = evaluate_relations({"A": a, "B": b}, [("A", "B")],
                              RelationConfig(cost_per_execution=0.0, borrow_per_day=0.0, min_trades=3))
    r = free["results"][0]
    assert r["discovery_gross_sum"] > 0 and r["stationary_window_share"] > 0.5
    costly = evaluate_relations({"A": a, "B": b}, [("A", "B")],
                                RelationConfig(cost_per_execution=0.01, min_trades=3))
    assert costly["results"][0]["verdict"] != "ESTADISTICA"
    assert costly["results"][0]["discovery_net_sum"] < costly["results"][0]["discovery_gross_sum"]


def test_execution_is_never_claimed_verifiable():
    a, b = _pair()
    r = evaluate_relations({"A": a, "B": b}, [("A", "B")])["results"][0]
    assert r["execution"].startswith("NO_VERIFICABLE")


def test_etf_groups_cover_equivalent_instruments_only():
    assert ("SPY", "IVV") in etf_pairs() and ("GLD", "IAU") in etf_pairs()
    assert all(not (x in ("SPY", "IVV", "VOO") and y in ("GLD", "IAU")) for x, y in etf_pairs())
