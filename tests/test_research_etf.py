import math
import random

import pytest

from lab.research.etf import RelationConfig, ccl_series, etf_pairs, evaluate_relations

D = 86_400_000


def test_ccl_ratio_is_verified_against_data_not_guessed():
    d1, d2 = D, 2 * D
    closes = {"GGAL": {d1: 37.0, d2: 37.2}, "GGAL.BA": {d1: 5950.0, d2: 5980.0},
              "BMA": {d1: 65.8, d2: 65.8}, "BMA.BA": {d1: 10600.0, d2: 10610.0},
              "YPF": {d1: 52.1, d2: 52.1}, "YPFD.BA": {d1: 8400.0, d2: 8400.0}}
    ccl, checks = ccl_series(closes, {"GGAL": ("GGAL.BA", 10), "BMA": ("BMA.BA", 10),
                                      "YPF": ("YPFD.BA", 1)})
    assert set(ccl) == {"GGAL", "BMA"}
    assert checks["YPF"].startswith("RATIO_NO_VERIFICADO")
    assert ccl["GGAL"][2 * D] == pytest.approx(5980 * 10 / 37.2)


def test_missing_series_are_reported():
    ccl, checks = ccl_series({"GGAL": {D: 1.0}}, {"GGAL": ("GGAL.BA", 10)})
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


def test_regression_daily_bars_with_different_exchange_hours_are_aligned_by_date():
    # Bug: NYSE marca 13:30 UTC y BYMA 14:00 UTC; por timestamp exacto no había días en común.
    day = 1_790_000_000_000 // D * D
    nyse = {day + 13 * 3_600_000 + 1_800_000: 37.0}
    byma = {day + 14 * 3_600_000: 5950.0}
    closes = {"GGAL": nyse, "GGAL.BA": byma, "BMA": {day + 48_600_000: 65.8},
              "BMA.BA": {day + 50_400_000: 10600.0}}
    ccl, checks = ccl_series(closes, {"GGAL": ("GGAL.BA", 10), "BMA": ("BMA.BA", 10)})
    assert set(ccl) == {"GGAL", "BMA"} and checks["GGAL"].startswith("OK")
