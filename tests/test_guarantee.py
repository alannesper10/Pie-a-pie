import json

import pytest

from src.guarantee import (
    EXEC_FAILED, EXEC_NOT_DEMONSTRATED, EXEC_VERIFIED, GUARANTEED, NO_EDGE, SPECULATIVE,
    UNVERIFIABLE, classify, kalshi_yes_coverage, load_manual_verified, no_subset_outcomes,
    scenario_table, simulate_leg_failure, strike_pair_outcomes, verify_execution,
    yes_all_outcomes,
)

T0 = "2026-10-13T08:42:00+00:00"
T1 = "2026-10-13T08:42:01+00:00"


def m(ticker, sub, rules="", **kw):
    return {"ticker": ticker, "yes_sub_title": sub, "rules_primary": rules, **kw}


def ev(title, markets, me=True, ticker="EV-1"):
    return {"event_ticker": ticker, "series_ticker": ticker.split("-")[0], "title": title,
            "mutually_exclusive": me, "markets": markets}


GAME = ev("City vs Ipswich", [
    m("A", "City", "If City wins the City vs Ipswich game, Yes."),
    m("B", "Ipswich", "If Ipswich wins the City vs Ipswich game, Yes."),
    m("T", "Tie", "If Tie is the result of the City vs Ipswich game, Yes.",
      rules_secondary="If the game is cancelled or rescheduled to over 48 hours away, "
                      "the market will resolve to a fair price in accordance with the rules.")])


# --- cobertura ---------------------------------------------------------------

def test_open_list_with_tie_is_not_covered_kxcriticscom_regression():
    films = [m(f"F{i}", f"Film {i}", f"If Film {i} has won Best Comedy, Yes.",
               early_close_condition="The market will close and expire early following "
                                     "nominations being released (if Film is not nominated)")
             for i in range(15)]
    cov = kalshi_yes_coverage(ev("Critics Choice Awards: Best Comedy",
                                 films + [m("TIE", "Tie", "If Tie has won Best Comedy, Yes.")]),
                              manual={})
    assert not cov.proven and cov.method == "NOT_PROVEN"
    assert cov.open_list_evidence                      # "if ... not nominated"
    assert any("no listado" in r for r in cov.reasons)


def test_other_option_alone_does_not_prove_coverage():
    cov = kalshi_yes_coverage(ev("Which AI first to 1550?", [
        m("Q", "Qwen", "If a model by Alibaba is the first to hit 1550 before 2027, Yes."),
        m("O", "Other", "If a model by Other is the first to hit 1550 before 2027, Yes.")]),
        manual={})
    assert not cov.proven                               # "nadie llega" no está cubierto


def test_head_to_head_with_tie_is_proven_and_lists_cancellation_residual():
    cov = kalshi_yes_coverage(GAME, manual={})
    assert cov.proven and cov.method == "HEAD_TO_HEAD_WITH_TIE"
    assert cov.residuals[0]["name"] == "CANCELACION_O_REPROGRAMACION"


def test_head_to_head_without_tie_market_is_not_proven():
    g = ev("A vs B", [m("A", "A", "If A wins"), m("B", "B", "If B wins")])
    assert not kalshi_yes_coverage(g, manual={}).proven


def test_ambiguous_rules_tie_market_must_describe_a_tie():
    g = ev("A vs B", [m("A", "A", "If A wins"), m("B", "B", "If B wins"),
                      m("T", "Tie", "If Tie has won Best Comedy, Yes.")])
    # "Tie" como opción de un premio, no empate del partido: no prueba nada.
    g["markets"][2]["rules_primary"] = "If the Tie entry wins the award, Yes."
    assert not kalshi_yes_coverage(g, manual={}).proven


def test_strike_partition_requires_same_variable():
    same = [m("L", "<60", "If the high temp is above # degrees", strike_type="less", cap_strike=60),
            m("H", ">60", "If the high temp is above # degrees", strike_type="greater", floor_strike=60)]
    assert kalshi_yes_coverage(ev("Temp", same), manual={}).method == "STRIKES_PARTITION"
    mixed = [dict(same[0]), dict(same[1], rules_primary="If the LOW temp is above # degrees")]
    assert not kalshi_yes_coverage(ev("Temp", mixed), manual={}).proven


def test_not_mutually_exclusive_is_never_covered():
    assert not kalshi_yes_coverage({**GAME, "mutually_exclusive": False}, manual={}).proven


def test_manual_verification_requires_who_and_when(tmp_path):
    p = tmp_path / "x.json"
    p.write_text(json.dumps({"events": [
        {"ticker": "EV-1", "verified": True, "verified_by": "alan", "verified_at": "2026-10-13"},
        {"ticker": "EV-2", "verified": True}]}))
    man = load_manual_verified(p)
    assert set(man) == {"EV-1"}
    films = ev("Awards", [m("F", "Film"), m("G", "Film 2")], ticker="EV-1")
    assert kalshi_yes_coverage(films, manual=man).method == "MANUAL_VERIFIED"


# --- escenarios --------------------------------------------------------------

def test_positive_expected_but_loss_in_uncovered_scenario_is_speculative():
    cov = kalshi_yes_coverage(ev("Awards", [m("F", "Film"), m("T", "Tie")]), manual={})
    t = scenario_table(yes_all_outcomes(9, cov), outlay=8.924)
    assert t["net_max"] == pytest.approx(0.076) and t["net_min"] == pytest.approx(-8.924)
    assert t["max_loss"] == pytest.approx(8.924)
    c, _ = classify(net_expected=0.076, coverage_proven=False, exec_status=EXEC_VERIFIED,
                    net_min=t["net_min"], net_min_stressed=t["net_min"])
    assert c == SPECULATIVE


def test_cancellation_is_listed_as_undetermined_payout():
    t = scenario_table(yes_all_outcomes(10, kalshi_yes_coverage(GAME, manual={})), 9.5)
    assert t["undetermined"] == ["CANCELACION_O_REPROGRAMACION"]
    assert t["net_min"] == pytest.approx(0.5)


def test_no_subset_and_strike_minimums():
    assert scenario_table(no_subset_outcomes(10, 3), 19.0)["net_min"] == pytest.approx(1.0)
    assert scenario_table(strike_pair_outcomes(10), 9.5)["net_min"] == pytest.approx(0.5)


def test_costs_turn_gross_profit_into_net_loss():
    c, _ = classify(net_expected=-0.01, coverage_proven=True, exec_status=EXEC_VERIFIED,
                    net_min=-0.01, net_min_stressed=-0.05)
    assert c == NO_EDGE


def test_assumed_costs_stressed_can_block_guarantee():
    c, why = classify(net_expected=0.02, coverage_proven=True, exec_status=EXEC_VERIFIED,
                      net_min=0.02, net_min_stressed=-0.01)
    assert c == UNVERIFIABLE and "x1.5" in why
    c, _ = classify(net_expected=0.2, coverage_proven=True, exec_status=EXEC_VERIFIED,
                    net_min=0.2, net_min_stressed=0.1)
    assert c == GUARANTEED


# --- ejecución ---------------------------------------------------------------

fee0 = lambda fills: 0.0  # noqa: E731


def leg(t, limit, asks, at=T1):
    return {"ticker": t, "side": "yes", "limit": limit, "asks_after": asks, "fetched_after": at}


def test_execution_verified_with_full_depth():
    r = verify_execution([leg("A", 0.5, [(0.5, 10)]), leg("B", 0.4, [(0.4, 10)])], 9, fee0)
    assert r["status"] == EXEC_VERIFIED and r["cost"] == pytest.approx(8.1)


def test_insufficient_depth_after_latency_fails():
    r = verify_execution([leg("A", 0.5, [(0.5, 10)]), leg("B", 0.4, [(0.4, 1), (0.45, 50)])], 9, fee0)
    assert r["status"] == EXEC_FAILED and "B" in r["reason"]      # 0.45 > límite 0.40


def test_missing_after_latency_book_is_not_demonstrated():
    r = verify_execution([leg("A", 0.5, [(0.5, 10)]), leg("B", 0.4, [], at=None)], 9, fee0)
    assert r["status"] == EXEC_NOT_DEMONSTRATED


def test_successive_queries_too_far_apart_are_not_simultaneous():
    r = verify_execution([leg("A", 0.5, [(0.5, 10)], at=T0),
                          leg("B", 0.4, [(0.4, 10)], at="2026-10-13T08:42:30+00:00")], 9, fee0)
    assert r["status"] == EXEC_NOT_DEMONSTRATED and r["skew_s"] == pytest.approx(30)
    c, _ = classify(net_expected=0.5, coverage_proven=True, exec_status=r["status"],
                    net_min=0.5, net_min_stressed=0.4)
    assert c == UNVERIFIABLE


def test_leg_failure_unwind_cost():
    r = verify_execution([leg("A", 0.5, [(0.5, 10)]), leg("B", 0.4, [(0.4, 10)])], 9, fee0)
    loss = simulate_leg_failure(r["legs"], lambda t, s: [(0.45, 100)], fail_index=1,
                                fee_fn=lambda f: 0.01 * len(f))
    # A se compró a 0.50 x9 = 4.50 y se vende a 0.45 x9 = 4.05 -> 0.45 + fees
    assert loss == pytest.approx(0.45 + 0.02)
