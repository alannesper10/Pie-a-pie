import math

from src.strategies import buy_all_no as ban
from src.strategies.kalshi_common import asks_for, parse_book


def mk(ticker, yes_bid, vol="500", status="active", result=""):
    return {"ticker": ticker, "market_type": "binary", "status": status,
            "result": result, "yes_bid_dollars": str(yes_bid),
            "volume_24h_fp": vol}


def event(markets, me=True):
    return {"event_ticker": "EV", "title": "t", "mutually_exclusive": me,
            "markets": markets}


def book(yes_bids=(), no_bids=()):
    return parse_book({"orderbook_fp": {
        "yes_dollars": [[f"{p:.4f}", f"{q}"] for p, q in yes_bids],
        "no_dollars": [[f"{p:.4f}", f"{q}"] for p, q in no_bids]}})


# --- libros: NO ask = 1 - YES bid ---

def test_no_ask_is_one_minus_yes_bid():
    b = book(yes_bids=[(0.40, 7), (0.35, 3)])
    assert asks_for(b, "no") == [(0.60, 7.0), (0.65, 3.0)]
    assert asks_for(b, "yes") == []          # sin NO bids no hay YES ask


# --- prefiltro ---

def test_requires_mutually_exclusive():
    ev = event([mk("A", 0.6), mk("B", 0.6)], me=False)
    assert ban.prefilter(ev)[1] == "NOT_MUTUALLY_EXCLUSIVE"


def test_does_not_require_exhaustiveness():
    # Sin "Tie"/"None" ni strikes: kalshi_current lo descartaría; acá sirve.
    pre, why = ban.prefilter(event([mk("A", 0.6), mk("B", 0.5)]))
    assert why == "OK" and len(pre["legs"]) == 2


def test_subset_drops_legs_without_contribution():
    ms = [mk("A", 0.55), mk("B", 0.50), mk("C", 0.001), mk("D", 0.0)]
    pre, _ = ban.prefilter(event(ms))
    assert {m["ticker"] for m in pre["legs"]} == {"A", "B"}


def test_already_determined_and_low_volume():
    ms = [mk("A", 0.6), mk("B", 0.5, result="yes")]
    assert ban.prefilter(event(ms))[1] == "ALREADY_DETERMINED"
    assert ban.prefilter(event([mk("A", 0.6, vol="1"), mk("B", 0.5, vol="1")]),
                         min_volume_24h=100)[1] == "LOW_VOLUME"


def test_prelim_gross_too_low():
    assert ban.prefilter(event([mk("A", 0.30), mk("B", 0.30)]))[1] == \
        "PRELIM_GROSS_TOO_LOW"


# --- evaluación con libros ---

def _eval(yes_bids_by_leg, **kw):
    ms = [mk(t, bids[0][0]) for t, bids in yes_bids_by_leg.items()]
    pre, why = ban.prefilter(event(ms))
    assert why == "OK", why
    books = {t: book(yes_bids=b) for t, b in yes_bids_by_leg.items()}
    return ban.evaluate(pre, books, **kw)


def test_min_payout_is_k_minus_one_and_net_edge():
    # 3 patas NO a 0.40/0.45/0.40 (YES bid 0.60/0.55/0.60): costo 1.25, paga >= 2.
    r = _eval({"A": [(0.60, 20)], "B": [(0.55, 20)], "C": [(0.60, 20)]},
              budget_usd=10)
    assert r.sides == ("no", "no", "no")
    assert r.min_payout_per_bundle == 2
    # Bruto 0.75/1.25 = 60% > 10% -> sospechoso, aunque sea "positivo".
    assert r.reason == "SUSPICIOUS_EDGE_CHECK_RULES" and not r.executable


def test_realistic_edge_is_executable_and_counts_fees_slippage():
    # NO asks 0.48 / 0.47: costo 0.95, paga >= 1 -> bruto 5.3%.
    r = _eval({"A": [(0.52, 30)], "B": [(0.53, 30)]}, slippage=0.001,
              budget_usd=10)
    assert r.executable and r.reason == "NET_EDGE_OK"
    assert r.contracts == 10                     # 10 x (0.95 + costos) <= 10
    assert math.isclose(r.cost, 9.5)
    assert r.min_payout == 10
    assert r.estimated_fees == 0.36             # ceil(0.07*10*.48*.52)+ceil(...*.47*.53)
    assert math.isclose(r.estimated_slippage, 0.02)
    assert math.isclose(r.net_profit, 10 - 9.5 - 0.36 - 0.02)


def test_positive_gross_is_not_enough():
    # NO asks 0.495 + 0.495 = 0.99: bruto +0.01, las comisiones lo matan.
    r = _eval({"A": [(0.505, 50)], "B": [(0.505, 50)]})
    assert not r.executable
    assert r.reason == "NO_POSITIVE_MARGINAL_EDGE"


def test_budget_too_small_with_many_legs():
    # 15 patas con YES bid 0.08 (suma 1.20): NO asks 0.92 -> costo 13.80,
    # paga >= 14. Hay edge neto, pero el paquete mínimo no entra en 10 USD.
    bids = {f"L{i}": [(0.08, 100)] for i in range(15)}
    r = _eval(bids, budget_usd=10)
    assert r.reason == "BUDGET_TOO_SMALL"
    assert not r.executable and r.contracts == 0
    assert r.min_payout_per_bundle == 14
    assert r.extra["fits_budget"] is False
    assert r.max_contracts_available >= 1        # existía edge marginal


def test_leg_with_tiny_bid_is_excluded_by_rounded_fee():
    # Regresión: YES bid 0.001 aporta 0.001 pero la comisión redondeada es 0.01.
    assert ban.leg_contribution(0.001, 0.07, 0.0) < 0
    assert ban.leg_contribution(0.30, 0.07, 0.0) > 0


def test_depth_partial_levels():
    r = _eval({"A": [(0.52, 3), (0.51, 50)], "B": [(0.53, 50)]}, budget_usd=100)
    # 3 paquetes al mejor nivel (0.48+0.47); después 0.49+0.47 = 0.96 sigue con edge.
    assert r.max_contracts_available > 3
    assert r.contracts == int(r.max_contracts_available)


def test_empty_book():
    ms = [mk("A", 0.52), mk("B", 0.53)]
    pre, _ = ban.prefilter(event(ms))
    r = ban.evaluate(pre, {"A": book(yes_bids=[(0.52, 5)]), "B": book()})
    assert not r.executable
