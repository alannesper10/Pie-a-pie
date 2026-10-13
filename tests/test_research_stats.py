import math
import random

import pytest

from lab.research.stats import (
    adf_tstat, bh_reject, eg_critical, half_life, ols, t_cdf, ttest_mean_gt0,
)


def test_t_cdf_known_values():
    assert t_cdf(0, 10) == pytest.approx(0.5)
    assert t_cdf(2.228, 10) == pytest.approx(0.975, abs=1e-3)   # tabla t: 0.975, df=10
    assert t_cdf(1.96, 10_000) == pytest.approx(0.975, abs=1e-3)
    assert t_cdf(-2.228, 10) == pytest.approx(0.025, abs=1e-3)


def test_one_sided_ttest():
    t, p = ttest_mean_gt0([0.1] * 5 + [0.2] * 5)
    assert t == pytest.approx(9.0) and p == pytest.approx(4.27e-6, rel=0.01)   # tabla t, df=9
    assert ttest_mean_gt0([-0.1, -0.2, -0.1])[1] > 0.9
    assert ttest_mean_gt0([1.0]) == (0.0, 1.0)


def test_ols_recovers_line():
    x = list(range(10))
    a, b, res = ols(x, [3 + 2 * xi for xi in x])
    assert a == pytest.approx(3) and b == pytest.approx(2) and max(map(abs, res)) < 1e-9


def test_adf_distinguishes_stationary_from_random_walk():
    rng = random.Random(1)
    ar = [0.0]
    for _ in range(600):
        ar.append(0.5 * ar[-1] + rng.gauss(0, 1))
    rw = [0.0]
    for _ in range(600):
        rw.append(rw[-1] + rng.gauss(0, 1))
    crit = eg_critical(600)
    assert crit == pytest.approx(-3.346, abs=0.01)
    assert adf_tstat(ar) < crit            # estacionaria: rechaza raíz unitaria
    assert adf_tstat(rw) > crit            # paseo aleatorio: no rechaza


def test_half_life():
    rng = random.Random(2)
    s = [0.0]
    for _ in range(2000):
        s.append(0.9 * s[-1] + rng.gauss(0, 0.1))
    assert half_life(s) == pytest.approx(math.log(2) / 0.1, rel=0.35)
    assert half_life([float(i) for i in range(50)]) is None


def test_benjamini_hochberg_controls_for_multiplicity():
    # 1 señal real + 19 nulas con p~uniforme: solo la real sobrevive.
    p = [0.0001] + [i / 20 for i in range(1, 20)]
    rej = bh_reject(p, q=0.10)
    assert rej[0] and sum(rej) == 1
    # Sin corrección, p<0.05 habría "descubierto" también p=0.05? no; pero 20
    # pruebas con p=0.04 cada una no sobreviven juntas si son nulas:
    assert sum(bh_reject([0.04] * 20, q=0.01)) == 0
