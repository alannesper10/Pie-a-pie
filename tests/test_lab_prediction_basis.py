import json
import logging

import pytest

from lab.core import LiquidityRegistry
from lab.fees import polymarket_fee
from lab.modules.basis import BasisFunding, RegistryBooks
from lab.modules.prediction import (
    CrossVenuePrediction, PolymarketBuyAllNo, bundle_walk, candidate_legs, cross_venue_edge,
    load_verified_pairs, select_tokens, suggest_pairs,
)
from tests.lab_fixtures import book, ctx, snap

SCHED = {"rate": 0.05, "exponent": 1, "takerOnly": True}


def pm_market(i, yes_bid, active=True):
    return {"id": str(i), "active": active, "closed": False, "enableOrderBook": True,
            "outcomes": '["Yes", "No"]', "bestBid": str(yes_bid), "orderMinSize": 5,
            "feeSchedule": SCHED, "tokens": [f"Y{i}", f"N{i}"]}


def pm_event(bids, slug="ev"):
    return {"slug": slug, "negRisk": True, "markets": [pm_market(i, b) for i, b in enumerate(bids)]}


def no_book(ask, size=100):
    return {"asks": [[ask, size]], "bids": [[ask - 0.01, size]]}


# --- comisiones Polymarket ---------------------------------------------------

def test_polymarket_fee_formula_and_status():
    c = polymarket_fee(100, 0.4, SCHED)
    assert c.usd == pytest.approx(100 * 0.05 * 0.4 * 0.6) and c.status == "VERIFIED"
    assert polymarket_fee(100, 0.4, None).status == "ASSUMED"
    assert polymarket_fee(100, 0.4, {"rate": 0}).usd == 0      # geopolítica sin fee


# --- buy_all_no en Polymarket ------------------------------------------------

def test_candidate_legs_filters_inactive_and_bad_outcomes():
    e = pm_event([0.5, 0.6])
    e["markets"].append(pm_market(9, 0.3, active=False))
    bad = pm_market(8, 0.3)
    bad["outcomes"] = '["No", "Yes"]'
    e["markets"].append(bad)
    assert [m["id"] for m in candidate_legs(e)] == ["0", "1"]
    assert select_tokens([e]) == ["N0", "N1"]


def test_bundle_min_payout_k_minus_one_and_fees():
    # NO asks 0.48 / 0.47: costo 0.95, paga >= 1.
    shares, cost, fees, fills = bundle_walk([[(0.48, 100)], [(0.47, 100)]], 1.0,
                                            [SCHED, SCHED], cap_usd=50, min_shares=5)
    assert shares == pytest.approx(52.63, abs=0.01)
    assert cost == pytest.approx(shares * 0.95)
    assert fees == pytest.approx(shares * 0.05 * (0.48 * 0.52 + 0.47 * 0.53), rel=1e-3)


def test_bundle_below_min_shares_is_zero():
    assert bundle_walk([[(0.48, 3)], [(0.47, 3)]], 1.0, [SCHED] * 2, 50, 5)[0] == 0


def _pm_snapshot(bids, no_asks, after_asks=None):
    e = pm_event(bids)
    books = {f"N{i}": no_book(a) for i, a in enumerate(no_asks)}
    after = {f"N{i}": no_book(a) for i, a in enumerate(after_asks or no_asks)}
    return snap({}, polymarket={"events": [e], "books": books, "books_after": after})


def test_polymarket_buy_all_no_estimated_and_executed():
    m, c = PolymarketBuyAllNo(), ctx("polymarket_buy_all_no")
    s = _pm_snapshot([0.52, 0.53], [0.48, 0.47])
    (o,) = m.evaluate(s, c)
    assert o.reason == "ESTIMATED_POSITIVE" and o.costs["fees_polymarket"].status == "VERIFIED"
    m.execute(o, s, c)
    assert o.decision == "ACCEPTED" and o.sim["realized"] is False
    assert o.sim["net_kind"] == "MINIMO_GARANTIZADO_A_RESOLUCION"
    assert c.ledger.locked == pytest.approx(o.sim["cost_usd"] + o.sim["fees_usd"])  # bloqueado


def test_polymarket_suspicious_edge():
    m, c = PolymarketBuyAllNo(), ctx("polymarket_buy_all_no")
    (o,) = m.evaluate(_pm_snapshot([0.7, 0.7], [0.30, 0.30]), c)
    assert o.reason == "SUSPICIOUS_EDGE_CHECK_RULES"


def test_polymarket_disappeared_after_latency():
    m, c = PolymarketBuyAllNo(), ctx("polymarket_buy_all_no")
    s = _pm_snapshot([0.52, 0.53], [0.48, 0.47], after_asks=[0.55, 0.55])
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "DISAPPEARED" and c.ledger.locked == 0


def test_polymarket_partial_leg_sells_excess_at_real_bid():
    m, c = PolymarketBuyAllNo(), ctx("polymarket_buy_all_no")
    s = _pm_snapshot([0.52, 0.53], [0.48, 0.47])
    s.polymarket["books_after"]["N1"] = {"asks": [[0.47, 10]], "bids": [[0.40, 100]]}
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "PARTIAL" and o.sim["matched_shares"] == pytest.approx(10)
    assert o.sim["unwind_usd"] > 0 and c.ledger.realized < 0


# --- Kalshi <-> Polymarket ---------------------------------------------------

def test_only_manually_verified_pairs_are_loaded(tmp_path):
    p = tmp_path / "pairs.json"
    p.write_text(json.dumps({"pairs": [
        {"kalshi_ticker": "A", "verified": True, "verified_by": "x", "verified_at": "2026-10-09"},
        {"kalshi_ticker": "B", "verified": True},                  # falta quién/cuándo
        {"kalshi_ticker": "C", "verified": False, "verified_by": "x", "verified_at": "d"}]}))
    assert [x["kalshi_ticker"] for x in load_verified_pairs(p)] == ["A"]
    assert load_verified_pairs(tmp_path / "no_existe.json") == []


def test_no_verified_pairs_means_no_opportunities():
    assert CrossVenuePrediction(pairs=[]).evaluate(snap({}), ctx("x")) == []


def test_cross_venue_edge_counts_both_fees():
    net, direction, cost, fees = cross_venue_edge(0.40, 0.62, 0.41, 0.55, SCHED, shares=10)
    assert direction == "YES_kalshi+NO_polymarket"
    assert cost == pytest.approx(9.5) and fees > 0 and net == pytest.approx(10 - 9.5 - fees)


def test_suggested_pairs_are_always_unverified():
    kev = [{"title": "Fed decision in October", "markets": [{"ticker": "KXFED-1", "yes_sub_title": "Hike 25bps"}]}]
    pev = [{"title": "Fed Decision in October?", "markets": [{"groupItemTitle": "25 bps increase", "question": "Fed hikes 25 bps?", "tokens": ["a", "b"]}]}]
    cands = suggest_pairs(kev, pev, min_score=0.3)
    assert cands and all(c["verified"] is False and c["status"] == "UNVERIFIED_CANDIDATE" for c in cands)


# --- basis_funding (envuelve funding/) ---------------------------------------

def test_registry_books_subtract_claimed_spot_liquidity():
    class A:
        def fetch_books(self, asset, limit=50):
            return {"spot_asks": [[100.0, 1.0]], "spot_bids": [[99.0, 1.0]],
                    "perp_bids": [[100.0, 1.0]], "perp_asks": [[100.1, 1.0]]}
    rb = RegistryBooks({"binance": A()})
    rb.registry = LiquidityRegistry()
    rb.registry.claim("binance", "BTC/USDT", "asks", [(100.0, 0.7)])
    assert rb.get("binance", "BTC")["spot_asks"] == [[100.0, pytest.approx(0.3)]]


def test_basis_module_maps_runner_snapshots(tmp_path):
    from funding.config import ASSUMED, FundingConfig, Param
    from funding.live import LiveRunner
    from funding.storage import Storage
    from tests.test_funding_live import FakeAdapter, SequenceBooks, book as fbook

    cfg = FundingConfig(assets=("BTC",), exchanges=("binance",),
                        leg_fail_prob=Param(0.0, ASSUMED, "t"))
    runner = LiveRunner(cfg, {"binance": FakeAdapter(0.0001)}, Storage(tmp_path / "f.sqlite"),
                        SequenceBooks([fbook()]), logging.getLogger("t"), sleep=lambda s: None)
    m = BasisFunding(db_path=None, runner=runner)
    (o,) = m.evaluate(snap({}), ctx("basis_funding"))
    assert o.reason == "EXPECTED_NET_NEGATIVE" and o.stage == "ESTIMATED"
    assert o.net_estimated_usd < 0 and "fee_spot_entrada" in o.costs
    assert o.observed["funding_rate"] == 0.0001
