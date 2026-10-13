import pytest

from lab.core import classify_lab
from lab.modules.cex_dex import CexDex, network_fee_usd
from lab.modules.term_structure import CalendarSpread, TermStructure
from lab.sources import FuturesSource
from src.guarantee import NO_EDGE, NOT_EXECUTABLE, UNVERIFIABLE
from tests.lab_fixtures import TS, book, ctx, snap

SOL = 100.0


def q(direction, usd, out_usd, min_frac=0.995):
    """Cotización de Jupiter: SOL->USDC devuelve USDC; USDC->SOL devuelve SOL."""
    if direction == "SOL->USDC":
        return {"in": int(usd / SOL * 1e9), "out": int(out_usd * 1e6),
                "min_out": int(out_usd * min_frac * 1e6), "slot": 1, "route": ["Raydium"]}
    return {"in": int(usd * 1e6), "out": int(out_usd / SOL * 1e9),
            "min_out": int(out_usd / SOL * min_frac * 1e9), "slot": 1, "route": ["Raydium"]}


def dex_snap(dex_out, cex_ask=100.0, cex_bid=99.95, after_out=None, fee=0):
    s = snap({"binance|SOL/USDC": book([(cex_bid, 50)], [(cex_ask, 50)])})
    s.dex = {"sol_usd": SOL, "priority_fee": {"median_micro_lamports_per_cu": fee},
             "quotes": {"SOL->USDC|25": q("SOL->USDC", 25, dex_out)},
             "quotes_after": {"SOL->USDC|25": q("SOL->USDC", 25, after_out or dex_out)}}
    return s


def test_network_fee_uses_observed_priority_and_assumed_cu():
    assert network_fee_usd({"median_micro_lamports_per_cu": 0}, 100) == pytest.approx(5000 / 1e9 * 100)
    assert network_fee_usd({"median_micro_lamports_per_cu": 10_000}, 100) > network_fee_usd({}, 100)


def test_quoted_price_is_not_the_guaranteed_price():
    # DEX paga 25.10 esperado (+0.4%), pero el mínimo garantizado (99.5%) es 24.97.
    m, c = CexDex(), ctx("cex_dex")
    (o,) = m.evaluate(dex_snap(25.10), c)
    assert o.costs["deslizamiento_dex_tolerado"].usd == pytest.approx(25.10 * 0.005, rel=1e-3)
    assert o.reason == "NET_NEGATIVE_AFTER_COSTS"           # bruto > 0, neto < 0
    assert classify_lab(o, "arbitrage")[0] == NO_EDGE


def test_real_gap_executes_with_minimum_out_and_requote():
    m, c = CexDex(), ctx("cex_dex", fail=0.0)
    m.tx_fail_prob = 0.0                                     # determinista
    s = dex_snap(26.0)                                       # +4% bruto
    (o,) = m.evaluate(s, c)
    assert o.reason == "ESTIMATED_POSITIVE"
    m.execute(o, s, c)
    assert o.reason == "FILLED"
    # se toma el MÍNIMO de la re-cotización tras la latencia
    assert o.sim["dex_quote_after"]["min_out"] == int(26.0 * 0.995 * 1e6)


def test_requote_after_latency_can_kill_it():
    m, c = CexDex(), ctx("cex_dex", fail=0.0)
    m.tx_fail_prob = 0.0                                     # determinista
    s = dex_snap(26.0, after_out=24.5)                       # el pool se movió
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "FILLED" and o.sim["net_usd"] < 0


def test_failed_onchain_tx_unwinds_cex_leg():
    m, c = CexDex(), ctx("cex_dex", fail=1.0)
    s = dex_snap(26.0)
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "LEG_FAILED" and o.sim["net_usd"] < 0


def test_missing_dex_quotes_produce_no_fake_opportunities():
    s = snap({"binance|SOL/USDC": book([(99.9, 50)], [(100, 50)])})
    assert CexDex().evaluate(s, ctx("cex_dex")) == []


# --- futuros con vencimiento -------------------------------------------------

DAY = 86_400_000
NOW = 1_791_900_000_000


def fut_snap(fut_bid, min_amount=0.0001, spot_ask=100.0, after=None, expiry_days=60):
    meta = {"deribit|BTC/USDC:USDC-261225": {
        "venue": "deribit", "asset": "BTC", "symbol": "BTC/USDC:USDC-261225", "spot": "BTC/USDC",
        "expiry": NOW + expiry_days * DAY, "expiry_iso": "2026-12-25T08:00:00Z",
        "contract_size": 1.0, "min_amount": min_amount, "min_cost": None,
        "taker_ref": 0.0005, "spot_min_amount": 0.0001, "spot_taker_ref": 0.001}}
    books = {"deribit|BTC/USDC": book([(spot_ask - 0.1, 10)], [(spot_ask, 10)]),
             "deribit|BTC/USDC:USDC-261225": book([(fut_bid, 10)], [(fut_bid + 0.1, 10)])}
    from datetime import datetime, timezone
    s = snap({}, ts=datetime.fromtimestamp(NOW / 1000, timezone.utc).isoformat())
    s.futures = {"books": books, "meta": meta, "books_after": after or books}
    return s


def test_cash_and_carry_locks_basis_and_reports_lock_period():
    m, c = TermStructure(), ctx("cash_and_carry", fail=0.0)
    s = fut_snap(102.0)                                      # base +2% a 60 días
    (o,) = m.evaluate(s, c)
    assert o.reason == "ESTIMATED_POSITIVE"
    assert o.lock_hours == pytest.approx(60 * 24) and o.valid_until
    assert o.max_loss_usd > 0
    assert "return_per_day_locked_pct" in o.observed and "annualized" not in str(o.observed)
    m.execute(o, s, c)
    assert o.reason == "FILLED" and o.sim["realized"] is False
    assert c.ledger.locked > 0                               # capital bloqueado hasta el vencimiento


def test_small_basis_does_not_cover_round_trip_costs():
    (o,) = TermStructure().evaluate(fut_snap(100.2), ctx("cash_and_carry"))
    assert o.reason == "NET_NEGATIVE_AFTER_COSTS"


def test_min_size_makes_it_not_executable_with_100_usd():
    (o,) = TermStructure().evaluate(fut_snap(102.0, min_amount=1.0), ctx("cash_and_carry"))
    assert o.reason == "INFEASIBLE_MIN_SIZE" and o.observed["min_capital_usd"] > 100
    assert classify_lab(o, "arbitrage")[0] in (NOT_EXECUTABLE, NO_EDGE)


def test_futures_leg_fails_leaves_unwind_loss():
    m, c = TermStructure(), ctx("cash_and_carry", fail=1.0)
    s = fut_snap(102.0)
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "LEG_FAILED" and o.sim["unwind_usd"] > 0


def test_calendar_spread_is_observation_never_arbitrage():
    s = fut_snap(102.0)
    s.futures["meta"]["deribit|BTC/USDC:USDC-270326"] = {
        **s.futures["meta"]["deribit|BTC/USDC:USDC-261225"], "symbol": "BTC/USDC:USDC-270326",
        "expiry": NOW + 150 * DAY}
    s.futures["books"]["deribit|BTC/USDC:USDC-270326"] = book([(104, 5)], [(104.2, 5)])
    (o,) = CalendarSpread().evaluate(s, ctx("calendar_spread"))
    assert o.reason == "OBSERVATION_NO_MODEL"
    assert classify_lab(o, "statistical")[0] == UNVERIFIABLE


class FakeFutEx:
    apiKey = ""

    def __init__(self):
        self.markets = {
            "BTC/USDT": {"limits": {"amount": {"min": 0.00001}}, "taker": 0.001},
            "BTC/USDT:USDT-261225": {"symbol": "BTC/USDT:USDT-261225", "future": True, "linear": True,
                                     "base": "BTC", "settle": "USDT", "expiry": NOW + 70 * DAY,
                                     "contractSize": 0.01, "limits": {"amount": {"min": 1}}},
            "BTC/USD:BTC-261225": {"symbol": "BTC/USD:BTC-261225", "future": True, "linear": False,
                                   "inverse": True, "base": "BTC", "settle": "BTC",
                                   "expiry": NOW + 70 * DAY},
            "BTC/USDT:USDT-261014": {"symbol": "BTC/USDT:USDT-261014", "future": True, "linear": True,
                                     "base": "BTC", "settle": "USDT", "expiry": NOW + DAY // 2}}

    def fetch_order_book(self, sym, depth):
        return {"bids": [[100.0, 3]], "asks": [[100.1, 3]]}


def test_futures_source_selects_linear_unexpired():
    src = FuturesSource(venues={"binance": ({}, "USDT")}, exchanges={"binance": FakeFutEx()},
                        now_ms=NOW)
    books, meta, errs = src.fetch()
    assert list(meta) == ["binance|BTC/USDT:USDT-261225"]   # ni inverso ni el que vence en <1 día
    # Binance lineal: el libro ya viene en BTC -> no se multiplica por contractSize
    assert books["binance|BTC/USDT:USDT-261225"]["bids"] == [[100.0, 3.0]]
    assert books["binance|BTC/USDT"]["bids"] == [[100.0, 3.0]]


def test_regression_deribit_linear_book_is_already_in_base_units():
    # Bug: se multiplicaba por contractSize=0.0001 y la profundidad quedaba 10.000x chica.
    src = FuturesSource(venues={"deribit": ({}, "USDT")}, exchanges={"deribit": FakeFutEx()},
                        now_ms=NOW)
    books, _, _ = src.fetch()
    assert books["deribit|BTC/USDT:USDT-261225"]["bids"] == [[100.0, 3.0]]


def test_okx_book_in_contracts_is_converted():
    src = FuturesSource(venues={"okx": ({}, "USDT")}, exchanges={"okx": FakeFutEx()}, now_ms=NOW)
    books, _, _ = src.fetch()
    assert books["okx|BTC/USDT:USDT-261225"]["bids"] == [[100.0, pytest.approx(0.03)]]


def test_cash_and_carry_tolerance_uses_t1_prices_for_net():
    m, c = TermStructure(), ctx("cash_and_carry", fail=0.0)
    s = fut_snap(102.0)
    after = {k: dict(v) for k, v in s.futures["books"].items()}
    after["deribit|BTC/USDC"] = book([(99.9, 10)], [(100.04, 10)])     # +4 bps: dentro de tolerancia
    s.futures["books_after"] = after
    (o,) = m.evaluate(s, c)
    m.execute(o, s, c)
    assert o.reason == "FILLED"
    assert o.sim["net_usd"] < o.net_estimated_usd                     # pagó el precio peor de T1
    after["deribit|BTC/USDC"] = book([(99.9, 10)], [(100.2, 10)])      # +20 bps: fuera
    m2, c2 = TermStructure(), ctx("cash_and_carry", fail=0.0)
    (o2,) = m2.evaluate(s, c2)
    m2.execute(o2, s, c2)
    assert o2.reason == "DISAPPEARED"
