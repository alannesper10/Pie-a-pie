"""Cash-and-carry histórico: convergencia, margen, salida anticipada, letra
del Tesoro y regla ex ante sin mirar el futuro."""

import pytest

from lab.research import carry
from lab.research.carry import (HOUR, ContractPrices, early_exit, ex_ante_net, fee_scale,
                                hold_to_expiry, margin_need, rate_at, rule_eval, simulate,
                                tbill_period_return)

DAY = 24 * HOUR


def test_tbill_period_return_uses_discount_basis_without_annualizing():
    r = tbill_period_return(4.0, 90)
    assert r == pytest.approx(0.01 / 0.99)
    assert tbill_period_return(4.0, 45) < r


def test_rate_at_never_looks_ahead():
    rates = {"2026-01-01": 4.0, "2026-01-03": 5.0}
    ts_jan2 = 1767312000000                      # 2026-01-02 00:00 UTC
    assert rate_at(rates, ts_jan2) == 4.0
    assert rate_at(rates, ts_jan2 - 2 * DAY) is None


def test_hold_to_expiry_locks_basis_and_measures_real_index_deviation():
    h = hold_to_expiry(s0=100.0, f0=101.0, spot_exit=150.0, delivery=150.3)
    assert h["gross_locked"] == pytest.approx(1.0)
    assert h["index_dev"] == pytest.approx(-0.3)            # vendimos el spot por debajo
    assert h["net"] == pytest.approx(1.0 - 0.3 - h["costs"])
    assert h["costs"] > 0


def test_early_exit_loses_when_basis_widens():
    assert early_exit(100, 101, 100, 103) < 0
    assert early_exit(100, 101, 100, 100.0) > early_exit(100, 101, 100, 103)


def test_margin_short_1x_liquidates_only_if_price_about_doubles():
    liq, extra = margin_need(f0=100.0, max_fut=150.0, leverage=1)
    assert not liq and extra == 0
    liq, extra = margin_need(f0=100.0, max_fut=200.0, leverage=1)
    assert liq and extra == pytest.approx(200 * carry.MMR)
    liq, _ = margin_need(f0=100.0, max_fut=150.0, leverage=2)  # 2x: 50% de suba alcanza
    assert liq


def test_fee_scale_increases_costs_and_restores():
    base = hold_to_expiry(100, 101, 100, 100)["costs"]
    with fee_scale(2.0):
        assert hold_to_expiry(100, 101, 100, 100)["costs"] > base
    assert hold_to_expiry(100, 101, 100, 100)["costs"] == pytest.approx(base)


def _market():
    """Dos vencimientos; el contrato E2 cotiza en NQ antes de E1 y en CQ después."""
    e1, e2 = 100 * DAY, 200 * DAY
    hours = range(0, e2 + HOUR, HOUR)
    spot = {t: 100.0 for t in hours}
    cq = {t: (101.0 if t < e1 else 100.5) for t in hours}       # tras el roll, CQ = contrato E2
    nq = {t: 102.0 for t in hours if t < e1}
    prices = ContractPrices({"CQ": (cq, {}), "NQ": (nq, {})}, [e1, e2])
    return spot, prices, {e1: 100.0, e2: 100.0}, [e1, e2]


def test_contract_prices_follow_the_same_contract_across_the_roll():
    spot, prices, deliv, exps = _market()
    assert prices.code(10 * DAY, exps[1]) == "NQ"
    assert prices.code(150 * DAY, exps[1]) == "CQ"
    assert prices.close(150 * DAY, exps[1]) == 100.5


def test_simulate_and_ex_ante_rule_do_not_use_future_information():
    spot, prices, deliv, exps = _market()
    rates = {"1970-01-01": 0.0}
    recs = simulate(spot, prices, deliv, exps, rates, step_hours=240, contract="NQ")
    assert recs and all(r["expiry"] == exps[1] for r in recs)
    r0 = recs[0]
    assert r0["basis_pct"] == pytest.approx(0.02)
    assert r0["ex_ante_net"] == pytest.approx(ex_ante_net(100.0, 102.0))
    # cambiar el precio de entrega (futuro) NO cambia la decisión ex ante
    recs2 = simulate(spot, prices, {exps[0]: 100.0, exps[1]: 90.0}, exps, rates, 240, "NQ")
    assert [r["ex_ante_excess_1x"] for r in recs2] == [r["ex_ante_excess_1x"] for r in recs]
    assert recs2[0]["net"] != r0["net"]
    rule = rule_eval(recs)
    assert rule["all"]["entries"] == len(recs)                  # tasa 0: todas superan la letra


def test_high_tbill_rate_blocks_entries():
    spot, prices, deliv, exps = _market()
    recs = simulate(spot, prices, deliv, exps, {"1970-01-01": 50.0}, 240, "NQ")
    assert rule_eval(recs)["all"]["entries"] == 0
