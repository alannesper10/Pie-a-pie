"""P4: carry G10 con diferencial de tasas real, ranking sin mirar el futuro y exclusión por tasa vieja."""

import pytest

from lab.research import fx_carry as fc


def flat_spot(months):
    return {c: {m: 1.0 for m in months} for c in fc.FX}


def test_ranking_uses_m_minus_2_rates_and_earns_m_minus_1_differential():
    months = ["2020-01", "2020-02", "2020-03", "2020-04"]
    spot = flat_spot(months)
    rates = {c: {m: 1.0 for m in ["2019-11", "2019-12"] + months} for c in list(fc.FX) + ["USD"]}
    for m in ["2019-11", "2019-12"] + months:
        rates["AUD"][m], rates["NZD"][m] = 5.0, 4.0           # las de mayor tasa
        rates["JPY"][m], rates["CHF"][m] = -0.5, 0.0          # las de menor tasa
    out = dict((m, (r, w)) for m, r, w in fc.run(spot, rates, cost_mult=0.0))
    r, w = out["2020-02"]
    assert w == {"JPY": -0.25, "CHF": -0.25, "AUD": 0.25, "NZD": 0.25}
    exp = 0.25 * ((5 - 1) + (4 - 1)) / 1200 - 0.25 * ((-0.5 - 1) + (0 - 1)) / 1200
    assert r == pytest.approx(exp)


def test_stale_rate_excludes_currency_and_costs_apply():
    months = ["2020-01", "2020-02", "2020-03"]
    spot = flat_spot(months)
    rates = {c: {m: 1.0 for m in ["2019-11", "2019-12"] + months} for c in list(fc.FX) + ["USD"]}
    rates["EUR"] = {"2019-01": 9.0}                            # muy vieja: excluida
    out = fc.run(spot, rates)
    assert all("EUR" not in w for _, _, w in out)
    assert fc.rate(rates, "EUR", "2019-03") == 9.0 and fc.rate(rates, "EUR", "2019-04") is None


def test_spot_move_counts_with_sign():
    months = ["2020-01", "2020-02"]
    spot = flat_spot(months)
    spot["AUD"]["2020-02"] = 1.10                                # AUD sube 10%
    rates = {c: {m: 1.0 for m in ["2019-11", "2019-12"] + months} for c in list(fc.FX) + ["USD"]}
    for m in rates["AUD"]:
        rates["AUD"][m] = 9.0
    r = [x for x in fc.run(spot, rates, cost_mult=0.0) if x[0] == "2020-02"][0][1]
    assert r == pytest.approx(0.25 * (0.10 + 8 / 1200))
