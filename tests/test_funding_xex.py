"""P3: diferencia de funding entre exchanges, con costos, precio relativo y exceso sobre la letra."""

import pytest

from lab.research import funding_xex as fx


def series(n, fa, fb, pa=100.0, pb=100.0):
    days = [f"2024-01-{i + 1:02d}" for i in range(n)]
    return days, {d: fa for d in days}, {d: fb for d in days}, {d: pa for d in days}, {d: pb for d in days}


def test_opens_short_on_high_funding_side_and_collects_difference_minus_costs():
    days, fa, fb, pa, pb = series(12, 0.0006, 0.0001)        # dif = 18,25% anual > 8%
    r = fx.simulate(days, fa, fb, pa, pb)
    assert r[6][1] == 0.0                                     # sin 7 días no decide
    cost = fx.FEE["binance"] + fx.FEE["bybit"] + 2 * fx.SLIP + fx.TRANSFER_PCT
    assert r[7][1] == pytest.approx(-cost)                    # abre al cierre del día 7
    assert r[8][1] == pytest.approx(0.0006 - 0.0001)          # cobra la diferencia desde el día siguiente


def test_relative_price_move_is_counted():
    days, fa, fb, pa, pb = series(10, 0.0006, 0.0001)
    pa[days[9]] = 101.0                                       # sube el perpetuo donde estamos cortos
    r = fx.simulate(days, fa, fb, pa, pb)
    assert r[9][1] == pytest.approx(0.0005 - 0.01)


def test_no_trade_below_threshold_and_excess_vs_tbill():
    days, fa, fb, pa, pb = series(14, 0.00012, 0.0001)       # 0,73% anual: no abre
    r = fx.simulate(days, fa, fb, pa, pb)
    assert all(x[1] == 0 and not x[2] for x in r)
    w = fx.weekly_excess(r, lambda d: 0.0001)
    assert w == [0.0, 0.0]                                    # sin posición no hay exceso (ni costo de oportunidad)
