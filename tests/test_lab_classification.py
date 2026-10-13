from lab.core import ASSUMED, VERIFIED, Cost, Opportunity, classify_lab
from src.guarantee import GUARANTEED, NO_EDGE, NOT_EXECUTABLE, STATISTICAL, UNVERIFIABLE


def opp(net_sim=None, status="FILLED", gross=1.0, costs=None, reason="FILLED"):
    o = Opportunity("cross_exchange", "k", 0, "t", ["a", "b"], ["BTC/USDT"], {},
                    gross_usd=gross, capital_usd=50, reason=reason,
                    costs=costs if costs is not None else {"fee": Cost(0.2, ASSUMED, "t")})
    if net_sim is not None:
        o.sim = {"status": status, "net_usd": net_sim}
    return o


def test_filled_and_robust_to_cost_stress_is_guaranteed():
    assert classify_lab(opp(0.5), "arbitrage")[0] == GUARANTEED


def test_assumed_costs_stress_blocks_guarantee():
    # neto 0.05 con 0.2 de costos supuestos: x1.5 -> 0.05 - 0.1 < 0
    assert classify_lab(opp(0.05), "arbitrage")[0] == UNVERIFIABLE


def test_verified_costs_are_not_stressed():
    o = opp(0.05, costs={"fee": Cost(0.2, VERIFIED, "API")})
    assert classify_lab(o, "arbitrage")[0] == GUARANTEED


def test_partial_or_failed_leg_is_not_executable():
    assert classify_lab(opp(0.5, status="PARTIAL", reason="PARTIAL"), "arbitrage")[0] == NOT_EXECUTABLE
    assert classify_lab(opp(-0.3, status="LEG_FAILED", reason="LEG_FAILED"), "arbitrage")[0] == NO_EDGE


def test_gross_positive_net_negative_is_no_edge():
    o = opp(None, gross=0.1, costs={"fee": Cost(0.3, ASSUMED, "t")}, reason="NET_NEGATIVE_AFTER_COSTS")
    assert classify_lab(o, "arbitrage")[0] == NO_EDGE


def test_regression_no_edge_is_not_mislabeled_unverifiable():
    # Bug: "NO_EDGE_AFTER_FEES_OR_MIN_SIZE" / "BUDGET_TOO_SMALL" con neto <= 0
    # se clasificaban NO_VERIFICABLE por contener "MIN_SIZE"/"BUDGET".
    for reason in ("NO_EDGE_AFTER_FEES_OR_MIN_SIZE", "BUDGET_TOO_SMALL"):
        o = opp(None, gross=0.1, costs={"fee": Cost(0.3, VERIFIED, "t")}, reason=reason)
        assert classify_lab(o, "arbitrage")[0] == NO_EDGE
    o = opp(None, gross=1.0, costs={"fee": Cost(0.1, VERIFIED, "t")}, reason="BUDGET_TOO_SMALL")
    assert classify_lab(o, "arbitrage")[0] == NOT_EXECUTABLE    # hay edge, no entra en capital
    assert classify_lab(opp(None, reason="NO_BOOK_FOR_LEG"), "arbitrage")[0] == UNVERIFIABLE


def test_stale_or_suspicious_is_unverifiable():
    assert classify_lab(opp(None, reason="STALE_BOOKS"), "arbitrage")[0] == UNVERIFIABLE
    assert classify_lab(opp(None, reason="SUSPICIOUS_SPREAD_CHECK_TRANSFERS"), "arbitrage")[0] == UNVERIFIABLE


def test_statistical_nature_is_never_guaranteed():
    assert classify_lab(opp(5.0), "statistical")[0] == STATISTICAL
    assert classify_lab(opp(5.0), "speculative")[0] == STATISTICAL      # alias histórico
    assert classify_lab(opp(-1.0), "statistical")[0] == NO_EDGE
    assert classify_lab(opp(5.0), "unverifiable")[0] == UNVERIFIABLE
