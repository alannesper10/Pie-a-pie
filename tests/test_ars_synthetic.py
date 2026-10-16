"""C6: dólar sintético, costos, base MEP/A3500 y rendimiento sobre margen separado."""

import pytest

from lab.research import ars_synthetic as asy


def test_no_move_no_gap_earns_peso_rate_minus_implied_and_costs():
    # A3500 y MEP quietos en 1000; futuro a 1010 (1% implícito); tasa 24% TNA, 30 días
    r = asy.cycle(1000, 1000.0, 1000.0, 1000.0, 1000.0, 1010.0, 24.0, 30, cost_mult=0.0)
    carry = 0.85 * 0.24 * 30 / 365 + 0.15 * 0.22 * 30 / 365
    assert r["ret_total_pct"] == pytest.approx((carry - 0.01) * 100)
    assert r["implied_cost_pct"] == pytest.approx(1.0) and r["basis_change_pct"] == pytest.approx(0.0)


def test_devaluation_is_hedged_by_futures():
    # el A3500 y el MEP suben 10%: el futuro compensa la pérdida de los pesos
    flat = asy.cycle(1000, 1000.0, 1000.0, 1000.0, 1000.0, 1010.0, 24.0, 30, cost_mult=0.0)["ret_total_pct"]
    dev = asy.cycle(1000, 1000.0, 1100.0, 1000.0, 1100.0, 1010.0, 24.0, 30, cost_mult=0.0)["ret_total_pct"]
    assert abs(dev - flat) < 1.0                          # cubierto (residuo por el carry en pesos)


def test_basis_risk_mep_vs_a3500_is_not_hedged():
    # el MEP se separa 5% del A3500 a la salida: pérdida que el futuro no cubre
    base = asy.cycle(1000, 1000.0, 1000.0, 1000.0, 1000.0, 1010.0, 24.0, 30, cost_mult=0.0)
    gap = asy.cycle(1000, 1000.0, 1050.0, 1000.0, 1000.0, 1010.0, 24.0, 30, cost_mult=0.0)
    assert gap["ret_total_pct"] < base["ret_total_pct"] - 4
    assert gap["mep_gap_exit_pct"] == pytest.approx(5.0)


def test_return_on_margin_is_reported_separately_with_costs():
    r = asy.cycle(1000, 1000.0, 1000.0, 1000.0, 1050.0, 1010.0, 24.0, 30)
    fut = 1000 * (1050 - 1010) - asy.FUT_FEE * 1000 * (1010 + 1050)
    assert r["fut_pnl_usd"] == pytest.approx(fut / 1000.0)
    assert r["ret_on_margin_pct"] == pytest.approx(fut / 1000.0 / 150 * 100)


def test_unexpired_contract_is_detected_by_final_settlement():
    assert asy.expired(1517.5209, 1517.5209)
    assert not asy.expired(1526.0, 1513.9308)          # DLR10/2026 al 15/10: aún no vence
    assert not asy.expired(1500.0, None)
