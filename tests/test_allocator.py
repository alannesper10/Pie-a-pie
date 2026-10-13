"""Asignador de capital: sin evidencia suficiente no hay capital."""

import pytest

from lab.allocator import MAX_SHARE, RESERVE, StrategyEvidence, allocate, gate


def ev(name, **kw):
    d = dict(name=name, realized_trades=40, periods=8, positive_period_share=0.75,
             net_return_per_capital_day=0.0005, oos_net=1.0, stress_net=0.5,
             max_loss_fraction=0.05, capacity_usd=1000.0)
    d.update(kw)
    return StrategyEvidence(**d)


def test_single_observation_never_gets_capital_even_with_huge_return():
    one = ev("carry_un_caso", realized_trades=1, periods=1, net_return_per_capital_day=0.5)
    a = allocate(100.0, [one])
    assert a["carry_un_caso"]["allocated_usd"] == 0 and not a["carry_un_caso"]["eligible"]
    assert gate(one)


def test_failing_oos_or_stress_blocks_allocation():
    assert allocate(100, [ev("a", oos_net=-0.1)])["a"]["allocated_usd"] == 0
    assert allocate(100, [ev("b", stress_net=0.0)])["b"]["allocated_usd"] == 0


def test_eligible_strategies_share_budget_with_caps_and_reserve():
    a = allocate(100.0, [ev("x"), ev("y", net_return_per_capital_day=0.001), ev("z", capacity_usd=5.0)])
    total = sum(v["allocated_usd"] for v in a.values())
    assert total <= 100 * (1 - RESERVE) + 1e-9
    assert all(v["allocated_usd"] <= 100 * MAX_SHARE + 1e-9 for v in a.values())
    assert a["z"]["allocated_usd"] == pytest.approx(5.0) and "capacidad" in a["z"]["capped_by"]
    assert a["y"]["allocated_usd"] >= a["x"]["allocated_usd"]
