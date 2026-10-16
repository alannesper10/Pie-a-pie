"""E1/E2: pesos sin mirar el futuro, neutralidad, funding y costos de rotación."""

import pytest

from lab.research import xsection as xs


def days(n):
    return [f"2024-{1 + i // 28:02d}-{1 + i % 28:02d}" for i in range(n)]


def test_momentum_longs_winners_shorts_losers_and_is_neutral():
    ds = days(40)
    closes = {f"C{i}": {d: 100 * (1 + 0.001 * i) ** k for k, d in enumerate(ds)} for i in range(10)}
    w = xs.momentum_weights(closes, 35, ds)
    assert sum(w.values()) == pytest.approx(0) and sum(abs(v) for v in w.values()) == pytest.approx(1)
    assert all(w[f"C{i}"] > 0 for i in (6, 7, 8, 9)) and all(w[f"C{i}"] < 0 for i in (0, 1, 2, 3))
    assert xs.momentum_weights(closes, 10, ds) == {}            # sin 30 días de historia


def test_reversal_weights_are_linear_and_dollar_neutral():
    ds = days(3)
    closes = {"A": {ds[0]: 100, ds[1]: 110}, "B": {ds[0]: 100, ds[1]: 90},
              "C": {ds[0]: 100, ds[1]: 100}, "D": {ds[0]: 100, ds[1]: 100}}
    w = xs.reversal_weights(closes, 1, ds)
    assert w["A"] == pytest.approx(-0.5) and w["B"] == pytest.approx(0.5) and w["C"] == pytest.approx(0)


def test_run_applies_weights_next_day_with_funding_and_turnover_costs():
    ds = days(3)
    closes = {"A": {ds[0]: 100, ds[1]: 110, ds[2]: 121}, "B": {ds[0]: 100, ds[1]: 90, ds[2]: 90},
              "C": {d: 100 for d in ds}, "D": {d: 100 for d in ds}}
    funding = {"A": {ds[2]: 0.001}}
    out = xs.run(closes, funding, ds, "reversal", cost=0.001)
    # día 1: sin pesos previos; se abren pesos -> costo de rotación 1·0,001
    assert out[0][1] == pytest.approx(-0.001)
    # día 2: A (−0,5) sube 10% y cobra funding como corto; B (+0,5) quieto
    w2 = xs.reversal_weights(closes, 2, ds)
    turn = sum(abs(w2.get(s, 0) - v) for s, v in {"A": -0.5, "B": 0.5, "C": 0.0, "D": 0.0}.items())
    assert out[1][1] == pytest.approx(-0.5 * 0.10 + 0.5 * 0.001 - turn * 0.001)
