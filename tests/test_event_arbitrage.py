import math

from src.event_arbitrage import (
    check_exhaustive,
    evaluate_event_bundle,
    prefilter_event,
    taker_fee,
    yes_asks_from_orderbook,
)


def mk(ticker, ask, sub="", vol="500", size="100", status="active", **kw):
    rules = ("If the game PSG vs Le Mans ends in a tie, then the market resolves to Yes."
             if sub.lower() == "tie" else f"If {sub} wins the PSG vs Le Mans game, then Yes.")
    m = {
        "ticker": ticker, "market_type": "binary", "status": status,
        "result": "", "yes_ask_dollars": str(ask), "yes_ask_size_fp": size,
        "volume_24h_fp": vol, "yes_sub_title": sub, "rules_primary": rules,
    }
    m.update(kw)
    return m


def event(markets, me=True, title="PSG vs Le Mans"):
    """Por defecto un partido 'A vs B' (cobertura demostrable con la pata de empate)."""
    return {"event_ticker": "EV", "title": title, "mutually_exclusive": me,
            "markets": markets}


def game(asks=(0.3, 0.3, 0.3), **kw):
    return [mk("A", asks[0], "PSG", **kw), mk("B", asks[1], "Le Mans", **kw),
            mk("T", asks[2], "Tie", **kw)]


def test_orderbook_bids_become_yes_asks():
    data = {"orderbook_fp": {"yes_dollars": [["0.30", "5"]],
                             "no_dollars": [["0.60", "10"], ["0.65", "4"]]}}
    assert yes_asks_from_orderbook(data) == [(0.35, 4.0), (0.40, 10.0)]


def test_old_cents_orderbook_format():
    data = {"orderbook": {"yes": [], "no": [[60, 10]]}}
    assert yes_asks_from_orderbook(data) == [(0.40, 10.0)]


def test_head_to_head_with_tie_is_proven():
    assert check_exhaustive(event(game())) == (True, "HEAD_TO_HEAD_WITH_TIE")


def test_regression_tie_is_not_a_catch_all_for_open_lists():
    # KXCRITICSCOM-27: premio con lista abierta + "Tie". Antes era exhaustivo.
    ms = [mk(f"F{i}", 0.05, f"Film {i}") for i in range(15)] + [mk("TIE", 0.02, "Tie")]
    ev = event(ms, title="Critics Choice Awards: Best Comedy")
    assert check_exhaustive(ev) == (False, "EXHAUSTIVENESS_UNCONFIRMED")


def test_other_does_not_cover_nobody_before_deadline():
    ev = event([mk("A", 0.3, "Claude"), mk("O", 0.1, "Other")], title="First AI to 1550")
    assert check_exhaustive(ev)[0] is False


def test_named_outcomes_without_catch_all_are_unconfirmed():
    ev = event([mk("A", 0.3, "Alice"), mk("B", 0.3, "Bob")], title="Who will win?")
    assert check_exhaustive(ev)[0] is False


def _strike(t, ask, st, **kw):
    return mk(t, ask, rules_primary="If the high temperature is above # degrees, then Yes.",
              strike_type=st, **kw)


def test_strike_ranges_covering_line():
    ev = event([
        _strike("L", 0.2, "less", cap_strike=60),
        _strike("M", 0.5, "between", floor_strike=60, cap_strike=70),
        _strike("H", 0.2, "greater", floor_strike=70),
    ], title="High temp")
    assert check_exhaustive(ev) == (True, "STRIKES_PARTITION")


def test_strike_ranges_with_gap_are_rejected_without_tolerance():
    ev = event([
        _strike("L", 0.2, "less", cap_strike=60),
        _strike("H", 0.2, "greater", floor_strike=61),
    ], title="High temp")
    assert check_exhaustive(ev)[0] is False
    assert check_exhaustive(ev, gap_tol=1)[0] is False      # gap_tol ya no relaja


def test_prefilter_rejects_non_exclusive_and_low_volume():
    ms = game()
    assert prefilter_event(event(ms, me=False))[1] == "NOT_MUTUALLY_EXCLUSIVE"
    assert prefilter_event(event(ms), min_volume_24h=10_000)[1] == "LOW_VOLUME"


def test_prefilter_skips_settled_no_legs_and_rejects_determined_events():
    ms = [mk("A", 0.4, "PSG"), mk("O", 0.5, "Tie"),
          mk("B", 0.0, "Le Mans", status="finalized", result="no")]
    pre, reason = prefilter_event(event(ms))
    assert reason == "OK" and pre.exhaustive_reason == "HEAD_TO_HEAD_WITH_TIE"
    assert pre.coverage["proven"] is True
    assert [m["ticker"] for m in pre.legs] == ["A", "O"]
    assert math.isclose(pre.prelim_sum, 0.9)

    ms[2]["result"] = "yes"
    assert prefilter_event(event(ms))[1] == "ALREADY_DETERMINED"


def test_prefilter_requires_open_legs_with_asks():
    ms = game()
    ms[0]["status"] = "closed"
    assert prefilter_event(event(ms))[1] == "LEG_NOT_TRADABLE"
    assert prefilter_event(event(game((1.0, 0.5, 0.3))))[1] == "LEG_WITHOUT_ASK"


def test_taker_fee_rounds_up_to_cent():
    assert taker_fee([(0.5, 1)], 0.07) == 0.02          # 0.0175 -> 0.02
    assert taker_fee([(0.5, 100)], 0.07) == 1.75


def _pre():
    return prefilter_event(event(game()), max_prelim_sum=10)[0]


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
