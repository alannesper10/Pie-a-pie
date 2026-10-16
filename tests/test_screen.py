"""Screening: sin mirar el futuro, costos por cambio de posición y split fijo."""

import pytest

from lab.research import screen as sc


def test_position_uses_only_past_and_applies_to_next_day():
    closes = [100.0] * 101 + [200.0]                  # el salto ocurre el último día
    pos = sc.positions(closes, "tsmom_20_100")
    assert pos[100] == -1.0 or pos[100] == 1.0
    # la posición del día del salto no puede haberse decidido con ese salto:
    d = [f"d{i:03d}" for i in range(len(closes))]
    rets = sc.backtest(d, closes, pos, 0.0)
    assert rets[-1][1] == pytest.approx(pos[-2] * 1.0)


def test_costs_charged_on_position_changes_and_carry():
    d = ["a", "b", "c", "d"]
    closes = [100.0, 100.0, 100.0, 100.0]
    pos = [1.0, -1.0, -1.0, 0.0]
    r = [x for _, x in sc.backtest(d, closes, pos, cost_turnover=0.001, carry_yr=0.0)]
    # día b: posición previa 1 desde 0 -> cambio 1; día c: de 1 a -1 -> cambio 2; día d: sin cambio
    assert r == pytest.approx([-0.001, -0.002, 0.0])
    r = [x for _, x in sc.backtest(d, closes, [1.0] * 4, 0.0, carry_yr=0.0252)]
    assert r[-1] == pytest.approx(-0.0001)


def test_funding_paid_by_longs_received_by_shorts():
    d = ["a", "b"]
    out = sc.backtest(d, [100.0, 100.0], [-1.0, -1.0], 0.0, funding=[0.0, 0.0003])
    assert out[0][1] == pytest.approx(0.0003 - 0.0)   # corto cobra funding (el costo de entrada se cuenta aparte)


def test_split_and_bonferroni_require_oos_and_is_positive():
    rets = [("2015-01-01", 0.01), ("2015-01-02", 0.02), ("2016-01-01", -0.01), ("2016-01-02", -0.02)]
    s = sc.split_stats(rets, "2015-12-31")
    assert s["in_sample"]["n"] == 2 and s["out_of_sample"]["n"] == 2
    b = sc.bonferroni({"x": s}, 0.05)
    assert b["pass"] == [] and b["t_crit_bonferroni"] == pytest.approx(1.96, abs=0.01)
