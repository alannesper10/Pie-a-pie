import math

from src.event_arbitrage import (
    check_exhaustive,
    evaluate_event_bundle,
    prefilter_event,
    taker_fee,
    yes_asks_from_orderbook,
)


def mk(ticker, ask, sub="", vol="500", size="100", status="active", **kw):
    return {
        "ticker": ticker, "market_type": "binary", "status": status,
        "result": "", "yes_ask_dollars": str(ask), "yes_ask_size_fp": size,
        "volume_24h_fp": vol, "yes_sub_title": sub, **kw,
    }


def event(markets, me=True):
    return {"event_ticker": "EV", "title": "t", "mutually_exclusive": me,
            "markets": markets}


def test_orderbook_bids_become_yes_asks():
    data = {"orderbook_fp": {"yes_dollars": [["0.30", "5"]],
                             "no_dollars": [["0.60", "10"], ["0.65", "4"]]}}
    assert yes_asks_from_orderbook(data) == [(0.35, 4.0), (0.40, 10.0)]


def test_old_cents_orderbook_format():
    data = {"orderbook": {"yes": [], "no": [[60, 10]]}}
    assert yes_asks_from_orderbook(data) == [(0.40, 10.0)]


def test_null_outcome_market_confirms_exhaustive():
    ev = event([mk("A", 0.3, "PSG"), mk("B", 0.3, "Le Mans"), mk("T", 0.3, "Tie")])
    assert check_exhaustive(ev) == (True, "CATCH_ALL_MARKET")


def test_other_does_not_cover_nobody_before_deadline():
    ev = event([mk("A", 0.3, "Claude"), mk("O", 0.1, "Other")])
    assert check_exhaustive(ev)[0] is False


def test_named_outcomes_without_catch_all_are_unconfirmed():
    ev = event([mk("A", 0.3, "Alice"), mk("B", 0.3, "Bob")])
    assert check_exhaustive(ev)[0] is False


def test_strike_ranges_covering_line():
    ev = event([
        mk("L", 0.2, strike_type="less", cap_strike=60),
        mk("M", 0.5, strike_type="between", floor_strike=60, cap_strike=70),
        mk("H", 0.2, strike_type="greater", floor_strike=70),
    ])
    assert check_exhaustive(ev) == (True, "STRIKES_COVER_RANGE")


def test_strike_ranges_with_gap_are_rejected_unless_tolerated():
    ev = event([
        mk("L", 0.2, strike_type="less", cap_strike=60),
        mk("H", 0.2, strike_type="greater", floor_strike=61),
    ])
    assert check_exhaustive(ev)[0] is False
    assert check_exhaustive(ev, gap_tol=1)[0] is True


def test_prefilter_rejects_non_exclusive_and_low_volume():
    ms = [mk("A", 0.3, "Alice"), mk("O", 0.1, "Tie")]
    assert prefilter_event(event(ms, me=False))[1] == "NOT_MUTUALLY_EXCLUSIVE"
    assert prefilter_event(event(ms), min_volume_24h=10_000)[1] == "LOW_VOLUME"


def test_prefilter_skips_settled_no_legs_and_rejects_determined_events():
    ms = [mk("A", 0.4, "Alice"), mk("O", 0.5, "Tie"),
          mk("B", 0.0, "Bob", status="finalized", result="no")]
    pre, reason = prefilter_event(event(ms))
    assert reason == "OK"
    assert [m["ticker"] for m in pre.legs] == ["A", "O"]
    assert math.isclose(pre.prelim_sum, 0.9)

    ms[2]["result"] = "yes"
    assert prefilter_event(event(ms))[1] == "ALREADY_DETERMINED"


def test_prefilter_requires_open_legs_with_asks():
    ms = [mk("A", 0.4, "Alice", status="closed"), mk("O", 0.5, "Tie")]
    assert prefilter_event(event(ms))[1] == "LEG_NOT_TRADABLE"
    ms = [mk("A", 1.0, "Alice"), mk("O", 0.5, "Tie")]
    assert prefilter_event(event(ms))[1] == "LEG_WITHOUT_ASK"


def test_taker_fee_rounds_up_to_cent():
    assert taker_fee([(0.5, 1)], 0.07) == 0.02          # 0.0175 -> 0.02
    assert taker_fee([(0.5, 100)], 0.07) == 1.75


def _pre(n=3):
    ms = [mk(f"M{i}", 0.3, f"x{i}") for i in range(n - 1)] + [mk("O", 0.3, "Tie")]
    return prefilter_event(event(ms), max_prelim_sum=10)[0]


def test_bundle_with_real_edge_is_executable():
    ladders = [[(0.30, 50)], [(0.30, 50)], [(0.30, 50)]]
    opp = evaluate_event_bundle(_pre(), ladders, fee_coefficient=0.07,
                                budget_usd=10)
    assert opp.executable
    assert opp.contracts == 11                  # 11 * 0.90 <= 10
    assert math.isclose(opp.pair_cost, 0.90)
    assert opp.net_profit > 0


def test_huge_edge_is_flagged_as_suspicious():
    ladders = [[(0.10, 50)], [(0.10, 50)], [(0.20, 50)]]   # suma 0.40
    opp = evaluate_event_bundle(_pre(), ladders, min_sane_ask_sum=0.90)
    assert not opp.executable
    assert opp.reason == "SUSPICIOUS_EDGE_CHECK_RULES"


def test_fees_kill_thin_edge():
    ladders = [[(0.33, 50)], [(0.33, 50)], [(0.33, 50)]]   # suma 0.99
    opp = evaluate_event_bundle(_pre(), ladders, fee_coefficient=0.07)
    assert not opp.executable
    assert opp.contracts == 0
    assert opp.reason == "NO_POSITIVE_MARGINAL_EDGE"


def test_depth_walk_stops_when_marginal_edge_disappears():
    ladders = [[(0.30, 5), (0.40, 100)], [(0.30, 100)], [(0.30, 100)]]
    opp = evaluate_event_bundle(_pre(), ladders, fee_coefficient=0.0)
    assert opp.max_contracts_available == 5     # 2do nivel suma 1.00
    assert opp.contracts == 5


def test_empty_leg_book():
    opp = evaluate_event_bundle(_pre(), [[(0.3, 5)], [], [(0.3, 5)]])
    assert not opp.executable
    assert opp.reason == "EMPTY_BOOK_ON_SOME_LEG"
