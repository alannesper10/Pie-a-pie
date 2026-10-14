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


# --- Regresión: data912 falla o devuelve datos inválidos (watch-b-20261013) ---
# Precios reales de la captura 191 (data912 caído): con el ratio público 1:1,
# YPFD 8.500 ARS vs YPF US$52,6 da un CCL implícito ~10 veces menor que el resto.

def byma_row(bid, ask, qb=1000, qa=1000):
    return {"bidPrice": bid, "offerPrice": ask, "quantityBid": qb, "quantityOffer": qa}


def nq_row(bid, ask, qb=100, qa=100):
    return {"bid": bid, "ask": ask, "bid_size": qb, "ask_size": qa}


BYMA_191 = {"YPFD|2": byma_row(8500, 8510, 8966, 586), "LOMA|2": byma_row(3195, 3202.5, 2791, 3418),
            "GGAL|2": byma_row(5820, 5835, 3103, 10655), "PAMP|2": byma_row(5225, 5230, 5816, 20),
            "GGAL|1": byma_row(1, 2)}                                  # otro plazo: se ignora
NQ_191 = {"YPF": nq_row(52.59, 52.63), "LOMA": nq_row(9.87, 9.91), "GGAL": nq_row(36.04, 36.1),
          "PAM": nq_row(80.74, 81.02)}
D912_OK = ({"GGAL": row(5820, 5835), "LOMA": row(3195, 3202.5), "PAMP": row(5225, 5230),
            "YPFD": row(8500, 8510)},
           {"GGAL": row(36.04, 36.1), "LOMA": row(9.87, 9.91), "PAM": row(80.74, 81.02),
            "YPF": row(52.59, 52.63)})


def snap(tick, data912=None):
    c = {"byma": BYMA_191, "nasdaq": NQ_191, "byma_fetched_at": "2026-10-14T16:50:00+00:00"}
    if data912:
        c.update({"arg_stocks": data912[0], "usa_adrs": data912[1],
                  "arg_stocks_fetched_at": "2026-10-14T16:50:00+00:00",
                  "usa_adrs_fetched_at": "2026-10-14T16:50:01+00:00"})
    return Snapshot(tick=tick, ts=f"2026-10-14T16:{50 + tick:02d}:00+00:00", ccl=c)


def test_defect_reproduced_unfiltered_byma_cross_gives_fictitious_906pct():
    """Con allowed=None (comportamiento anterior al fallar data912) aparece el
    +906%: es el defecto. El filtro nuevo nunca debe dejarlo pasar."""
    lq = {k.split("|")[0]: (v["bidPrice"], v["quantityBid"], v["offerPrice"], v["quantityOffer"])
          for k, v in BYMA_191.items() if k.endswith("|2")}
    aq = {k: (v["bid"], v["bid_size"], v["ask"], v["ask_size"]) for k, v in NQ_191.items()}
    old = max(p["gross"] for p in ccl.ccl_pairs(lq, aq, allowed=None))
    assert old > 8.0                     # ~ +896% con estas puntas (+906% en la corrida)
    obs = ccl.analyze_snapshot(snap(0))
    assert obs and max(o["gross"] for o in obs if o["gross"] is not None) < ccl.SUSPICIOUS_GROSS


def test_data912_down_byma_cross_excludes_inconsistent_ratio_and_is_not_verifiable():
    obs = ccl.analyze_snapshot(snap(0))                                # sin data912
    assert ccl.byma_ratio_check(snap(0))["YPF"]["status"] == "NO_CONSISTENTE"
    assert all("YPF" not in (o["sell_usd_in"], o["buy_usd_in"]) for o in obs)
    assert {o["source"] for o in obs} == {"byma_demorado+nasdaq"}
    assert {o["verdict"] for o in obs} == {"NO_VERIFICABLE"}
    assert not [o for o in obs if o["verdict"] in ("POTENCIAL", "SOSPECHOSO_REVISAR_DATOS")]


def test_ratio_without_any_verification_is_not_verifiable_and_has_no_numbers():
    s = Snapshot(tick=0, ts="2026-10-14T16:50:00+00:00",
                 ccl={"byma": {"GGAL|2": BYMA_191["GGAL|2"], "YPFD|2": BYMA_191["YPFD|2"]},
                      "nasdaq": {"GGAL": NQ_191["GGAL"], "YPF": NQ_191["YPF"]}})
    assert ccl.byma_ratio_check(s) == {}                    # 2 emisoras: sin mediana confiable
    obs = ccl.analyze_snapshot(s)
    assert obs and all(o["verdict"] == "NO_VERIFICABLE" and o["reason"] == "RATIO_NO_VERIFICADO"
                       and o["gross"] is None and o["net"] is None for o in obs)
    summ = ccl.summarize(obs)["CCL|byma_demorado+nasdaq"]
    assert summ["gross_max"] is None and summ["verdicts"] == {"NO_VERIFICABLE": 2}
    assert ccl.episodes(obs) == []


def test_data912_invalid_values_never_create_edge():
    bad_stocks = {"GGAL": row("n/d", 5835), "LOMA": row(float("nan"), 3202.5), "PAMP": row(-5225, 5230),
                  "YPFD": row(8500, 8510), "GGALD": row(0, 4.0), "PAMPD": row(3.5, None)}
    bad_adrs = {"GGAL": row(36.04, 36.1), "LOMA": row(9.87, 9.91), "PAM": row(80.74, 81.02),
                "YPF": row(52.59, 52.63)}
    obs = ccl.analyze_snapshot(snap(0, (bad_stocks, bad_adrs)))
    d912 = [o for o in obs if o["source"] == "data912"]
    assert d912 == []                         # sin ratio verificable ni puntas válidas: nada
    assert ccl.mep_pairs(bad_stocks) == []
    assert all("YPF" not in (o["sell_usd_in"], o["buy_usd_in"]) for o in obs)
    assert not [o for o in obs if o["verdict"] in ("POTENCIAL", "SOSPECHOSO_REVISAR_DATOS")]


def test_crossed_quotes_are_invalid_not_an_edge():
    lq = {"GGAL": (6000, 500, 6010, 500), "PAMP": (5300, 2500, 5210, 2500)}       # PAMP cruzada
    aq = {"GGAL": (37.0, 50, 37.1, 50), "PAM": (81.0, 50, 81.2, 50)}
    assert ccl.ccl_pairs(lq, aq) == []
    stocks = {"GGAL": row(6000, 6010), "GGALD": row(4.02, 4.00),                  # D cruzada
              "PAMP": row(5200, 5210), "PAMPD": row(3.50, 3.51)}
    assert ccl.mep_pairs(stocks) == []


def test_source_fails_then_recovers():
    seq = [snap(0, D912_OK), snap(1), snap(2, ({}, {})), snap(3, D912_OK)]
    per = [ccl.analyze_snapshot(s) for s in seq]
    for obs in per:                                  # YPF nunca participa, nunca hay edge ficticio
        assert all("YPF" not in (o["sell_usd_in"], o["buy_usd_in"]) for o in obs)
        assert not [o for o in obs if o["verdict"] in ("POTENCIAL", "SOSPECHOSO_REVISAR_DATOS")]
    has912 = [any(o["source"] == "data912" for o in obs) for obs in per]
    assert has912 == [True, False, False, True]      # caído o vacío: sin cifras de data912
    assert all(any(o["source"] == "byma_demorado+nasdaq" for o in obs) for obs in per)


def test_byma_allowed_needs_consistency_and_any_inconsistency_excludes():
    ok, bad = {"status": "CONSISTENTE"}, {"status": "NO_CONSISTENTE"}
    allowed, unverified = ccl.byma_allowed({"GGAL": ok, "YPF": ok}, {"GGAL": ok, "YPF": bad})
    assert allowed == {"GGAL"} and "YPF" not in unverified and "BMA" in unverified
    allowed, _ = ccl.byma_allowed({}, {})
    assert allowed == set()
