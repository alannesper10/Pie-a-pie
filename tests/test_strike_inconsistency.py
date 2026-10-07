import math

from src.strategies import strike_inconsistency as si
from src.strategies.kalshi_common import parse_book


def mk(ticker, strike, ask, bid, rules, st="greater", vol="500", status="active"):
    m = {"ticker": ticker, "strike_type": st, "status": status, "result": "",
         "yes_ask_dollars": str(ask), "yes_bid_dollars": str(bid),
         "volume_24h_fp": vol, "rules_primary": rules, "market_type": "binary"}
    m["floor_strike" if st in si.GREATER else "cap_strike"] = strike
    return m


def event(markets, ticker="EV"):
    return {"event_ticker": ticker, "mutually_exclusive": False, "markets": markets}


def book(yes_bids=(), no_bids=()):
    return parse_book({"orderbook_fp": {
        "yes_dollars": [[f"{p:.4f}", f"{q}"] for p, q in yes_bids],
        "no_dollars": [[f"{p:.4f}", f"{q}"] for p, q in no_bids]}})


# --- normalización ---

def test_rules_template_masks_numbers_with_commas_and_units():
    a = si.rules_template("If Derrick Henry records at least 14,000 career yards")
    b = si.rules_template("If Derrick Henry records at least 15,500.5 career  yards")
    assert a == b == "if derrick henry records at least # career yards"
    assert si.rules_template("above 5.75% by $1,000") == "above # by #"


def test_ticker_stem():
    assert si.ticker_stem("KXNCAAFTEAMTOTAL-26OCT10BALLNW-BALL20") == \
        "KXNCAAFTEAMTOTAL-26OCT10BALLNW-BALL"
    assert si.ticker_stem("KXMLBTB-26OCT071600CLECWS-CLEAMARTNEZ1-2") == \
        "KXMLBTB-26OCT071600CLECWS-CLEAMARTNEZ1"
    assert si.ticker_stem("KXBRINFHIGH-27JAN01-T5.75") == "KXBRINFHIGH-27JAN01-T"


# --- REGRESIÓN del bug de 14.274 falsos candidatos ---

def test_regression_player_props_never_mix_players():
    # Forma real de KXMLBTB-26OCT071600CLECWS: un evento con escaleras de
    # varios jugadores. El bug comparaba ">2.5 de Martínez" contra ">3.5 de
    # Rocchio" y veía +0.94. Con la agrupación correcta: CERO candidatos.
    ev = "KXMLBTB-26OCT071600CLECWS"
    r_am = "If Angel Martínez records {} or more total bases, then yes."
    r_br = "If Brayan Rocchio records {} or more total bases, then yes."
    ms = [
        mk(f"{ev}-CLEAMARTNEZ1-3", 2.5, 0.05, 0.01, r_am.format(3)),
        mk(f"{ev}-CLEAMARTNEZ1-4", 3.5, 0.04, 0.01, r_am.format(4)),
        mk(f"{ev}-CLEBROCCHIO4-3", 2.5, 0.995, 0.99, r_br.format(3)),
        mk(f"{ev}-CLEBROCCHIO4-4", 3.5, 0.995, 0.99, r_br.format(4)),
    ]
    groups, reasons = si.build_groups(event(ms, ev))
    assert len(groups) == 2
    assert all(len({si.ticker_stem(m["ticker"]) for m in g}) == 1 for g in groups)
    cands, _ = si.candidates_for_event(event(ms, ev))
    # Solo pares del MISMO jugador (Rocchio vs Rocchio es un casi-acierto
    # legítimo) y ninguno con ganancia bruta positiva.
    assert all(si.ticker_stem(c["broad"]["ticker"]) == si.ticker_stem(c["narrow"]["ticker"])
               for c in cands)
    assert [c for c in cands if c["gross_top"] > 0] == []


def test_regression_team_totals_with_glued_ticker_numbers():
    # Forma real de KXNCAAFTEAMTOTAL: el número va pegado al equipo
    # (BALL20 / NW23). El primer intento de arreglo seguía mezclando equipos.
    ev = "KXNCAAFTEAMTOTAL-26OCT10BALLNW"
    rb = "If Ball State scores more than {} points, then yes."
    rn = "If Northwestern scores more than {} points, then yes."
    ms = [
        mk(f"{ev}-BALL20", 20.5, 0.06, 0.05, rb.format(20.5)),
        mk(f"{ev}-BALL23", 23.5, 0.03, 0.02, rb.format(23.5)),
        mk(f"{ev}-NW20", 20.5, 0.97, 0.96, rn.format(20.5)),
        mk(f"{ev}-NW23", 23.5, 0.97, 0.96, rn.format(23.5)),
    ]
    cands, _ = si.candidates_for_event(event(ms, ev))
    assert all(c["broad"]["ticker"][:-2] == c["narrow"]["ticker"][:-2] for c in cands)
    assert [c for c in cands if c["gross_top"] > 0] == []


def test_same_stem_different_rules_is_grouping_mismatch():
    ms = [mk("EV-X-1", 1, 0.5, 0.4, "If A scores # points"),
          mk("EV-X-2", 2, 0.5, 0.4, "If A scores # points"),
          mk("EV-X-3", 3, 0.5, 0.4, "If B scores # goals")]
    groups, reasons = si.build_groups(event(ms))
    assert groups == [] and reasons["GROUPING_MISMATCH"] >= 1


def test_same_rules_different_stems_is_grouping_mismatch():
    ms = [mk("EV-A1", 1, 0.5, 0.4, "If the value is above #"),
          mk("EV-B2", 2, 0.5, 0.4, "If the value is above #")]
    groups, reasons = si.build_groups(event(ms))
    assert groups == [] and reasons["GROUPING_MISMATCH"] == 1


def test_duplicate_strike_is_ambiguous():
    ms = [mk("EV-T1", 1, 0.5, 0.4, "above #"), mk("EV-T1.0", 1, 0.5, 0.4, "above #")]
    groups, reasons = si.build_groups(event(ms))
    assert groups == [] and reasons["AMBIGUOUS_GROUP"] == 1


def test_different_events_never_mix():
    a = event([mk("E1-T1", 1, 0.05, 0.04, "above #")], "E1")
    b = event([mk("E2-T2", 2, 0.95, 0.90, "above #")], "E2")
    assert si.candidates_for_event(a)[0] == [] and si.candidates_for_event(b)[0] == []


# --- dirección de los pares ---

def test_greater_pair_direction():
    ms = [mk("EV-T1", 1, 0.40, 0.38, "above #"), mk("EV-T2", 2, 0.45, 0.42, "above #")]
    cands, _ = si.candidates_for_event(event(ms))
    (c,) = cands
    assert c["broad"]["ticker"] == "EV-T1" and c["narrow"]["ticker"] == "EV-T2"
    assert math.isclose(c["gross_top"], 0.02)   # bid(>2) 0.42 - ask(>1) 0.40


def test_less_pair_direction():
    ms = [mk("EV-T1", 1, 0.45, 0.42, "below #", st="less"),
          mk("EV-T2", 2, 0.40, 0.38, "below #", st="less")]
    (c,) = si.candidates_for_event(event(ms))[0]
    assert c["broad"]["ticker"] == "EV-T2" and c["narrow"]["ticker"] == "EV-T1"


# --- evaluación ---

def _evaluate(ask_b, bid_n, size=50, **kw):
    ms = [mk("EV-T1", 1, ask_b, ask_b - 0.01, "above #"),
          mk("EV-T2", 2, bid_n + 0.01, bid_n, "above #")]
    (c,) = si.candidates_for_event(event(ms))[0]
    books = {"EV-T1": book(no_bids=[(1 - ask_b, size)]),
             "EV-T2": book(yes_bids=[(bid_n, size)])}
    return si.evaluate(c, books, **kw)


def test_inconsistency_buys_yes_broad_and_no_narrow_min_payout_one():
    r = _evaluate(0.40, 0.46, budget_usd=10)   # bruto 0.06 / 0.94 = 6.4%
    assert r.sides == ("yes", "no")
    assert r.min_payout_per_bundle == 1.0
    assert math.isclose(r.best_bundle_cost, 0.40 + 0.54)
    assert r.executable and r.contracts == 10


def test_small_inconsistency_killed_by_fees():
    r = _evaluate(0.40, 0.43)                    # bruto 0.03 < comisiones ~0.034
    assert not r.executable and r.reason == "NO_POSITIVE_MARGINAL_EDGE"


def test_gross_over_ten_percent_is_suspicious():
    r = _evaluate(0.05, 0.99)                    # el patrón del bug
    assert r.reason == "SUSPICIOUS_EDGE_CHECK_RULES" and not r.executable


def test_regression_fractional_top_size_is_insufficient_depth():
    # Caso real KXGOVTCUTS-28-1|500: edge en el top pero solo 0.13 contratos.
    from src.strategies.kalshi_common import is_net_positive
    r = _evaluate(0.05, 0.08, size=0.13)
    assert r.reason == "INSUFFICIENT_DEPTH" and not r.executable
    assert not is_net_positive(r)
    r = _evaluate(0.05, 0.08, size=5)
    assert r.executable and is_net_positive(r)
