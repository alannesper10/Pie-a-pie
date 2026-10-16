"""E4: AUD.CAD lineal acotado con rollover real y costos."""

import pytest

from lab.research import fx_pair as fp


def test_position_is_minus_half_z_capped_and_applied_next_day():
    dates = [f"2020-01-{i + 1:02d}" for i in range(25)]
    px = {d: 1.0 for d in dates}
    for i, d in enumerate(dates):
        px[d] = 1.0 + 0.001 * (i % 2)
    px[dates[21]] = 1.05                                              # salto: z muy alto -> posición −1
    px[dates[22]] = 1.0
    out = dict(fp.run(dates, px, lambda d: 0.0, lambda d: 0.0, cost_mult=0.0))
    assert out[dates[22]] == pytest.approx(-1.0 * (1.0 / 1.05 - 1))    # corto AUD gana la reversión


def test_rollover_differential_accrues_with_sign():
    dates = [f"2020-01-{i + 1:02d}" for i in range(25)]
    px = {d: 1.0 + 0.001 * (i % 2) for i, d in enumerate(dates)}
    px[dates[21]] = 0.95                                              # z muy bajo -> largo AUD (+1)
    out = dict(fp.run(dates, px, lambda d: 4.0, lambda d: 1.0, cost_mult=0.0))
    r = out[dates[22]]
    assert r == pytest.approx(px[dates[22]] / 0.95 - 1 + 0.03 / 365)   # cobra el diferencial AUD − CAD
