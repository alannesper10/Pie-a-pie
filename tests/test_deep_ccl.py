"""Diferenciales de dólar implícito entre emisoras (MEP y CCL) con puntas."""

import pytest

from lab.research import ccl
from lab.sources import Snapshot


def row(bid, ask, qb=1000, qa=1000):
    return {"px_bid": bid, "px_ask": ask, "q_bid": qb, "q_ask": qa}


def test_mep_uses_executable_sides_and_four_byma_trades():
    stocks = {"GGAL": row(6000, 6010), "GGALD": row(4.00, 4.01),
              "PAMP": row(5200, 5210), "PAMPD": row(3.50, 3.51)}
    pairs = {(p["sell_usd_in"], p["buy_usd_in"]): p for p in ccl.mep_pairs(stocks)}
    p = pairs[("GGAL", "PAMP")]
    assert p["gross"] == pytest.approx((6000 / 4.01) / (5210 / 3.50) - 1)
    assert p["net"] == pytest.approx(p["gross"] - 4 * ccl.cost_per_trade_ar())
    assert ccl.BYMA_MARKET_FEE == pytest.approx(0.0005 * 1.21)


def test_ccl_pairs_apply_ratio_and_capacity_in_usd():
    lq = {"GGAL": (6000, 500, 6010, 500), "PAMP": (5200, 2500, 5210, 2500)}
    aq = {"GGAL": (37.0, 50, 37.1, 50), "PAM": (81.0, 50, 81.2, 50)}
    pairs = {(p["sell_usd_in"], p["buy_usd_in"]): p for p in ccl.ccl_pairs(lq, aq)}
    p = pairs[("GGAL", "PAM")]
    sell = 6000 * 10 / 37.1                   # vender local (bid) / comprar ADR (ask)
    buy = 5210 * 25 / 81.0                    # comprar local (ask) / vender ADR (bid)
    assert p["gross"] == pytest.approx(sell / buy - 1)
    assert p["usd_capacity"] == pytest.approx(min(50 * 37.1, min(2500 / 25, 50) * 81.0))


def test_inconsistent_ratio_is_excluded_and_huge_edges_are_suspicious():
    stocks = {"GGAL": row(6000, 6010), "GGALD": row(4.00, 4.01), "BMA": row(10600, 10620),
              "PAMP": row(5200, 5210), "YPFD": row(8300, 8310)}           # YPF inconsistente
    adrs = {"GGAL": row(37.0, 37.05), "BMA": row(66.0, 66.1), "PAM": row(81.0, 81.1),
            "YPF": row(51.7, 51.8)}
    s = Snapshot(tick=0, ts="2026-10-13T19:00:00+00:00",
                 ccl={"arg_stocks": stocks, "usa_adrs": adrs,
                      "arg_stocks_fetched_at": "2026-10-13T19:00:00+00:00",
                      "usa_adrs_fetched_at": "2026-10-13T19:00:01+00:00"})
    rc = ccl.ratio_check(s)
    assert rc["YPF"]["status"] == "NO_CONSISTENTE" and rc["GGAL"]["status"] == "CONSISTENTE"
    obs = [o for o in ccl.analyze_snapshot(s) if o["kind"] == "CCL"]
    assert obs and all("YPF" not in (o["sell_usd_in"], o["buy_usd_in"]) for o in obs)
    assert ccl.classify({"gross": 0.5, "net": 0.49}, 0.0, 0.4) == "SOSPECHOSO_REVISAR_DATOS"


def test_non_simultaneous_quotes_are_not_verifiable():
    p = {"gross": 0.02, "net": 0.01}
    assert ccl.classify(p, None, 0.005) == "NO_VERIFICABLE"
    assert ccl.classify(p, 120, 0.005) == "NO_VERIFICABLE"
    assert ccl.classify(p, 1, 0.005) == "POTENCIAL"
    assert ccl.classify(p, 1, -0.001) == "SIN_EDGE"          # no resiste costos x1,5


def test_episodes_merge_consecutive_ticks_without_double_counting():
    base = {"kind": "CCL", "source": "data912", "sell_usd_in": "A", "buy_usd_in": "B",
            "verdict": "POTENCIAL", "net": 0.01, "usd_capacity": 100}
    obs = [{**base, "tick": t, "ts": str(t)} for t in (1, 2, 3, 7)]
    eps = ccl.episodes(obs)
    assert sorted(e["ticks"] for e in eps) == [1, 3]
