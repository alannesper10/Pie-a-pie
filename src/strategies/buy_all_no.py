"""buy_all_no: comprar NO en un subconjunto de patas de un evento
mutuamente excluyente.

Matemática: si a lo sumo una pata resuelve YES, k patas NO pagan como mínimo
k - 1 (y k si no gana ninguna). NO necesita exhaustividad. Tampoco necesita
todas las patas: cada pata aporta (1 - NO_ask) - comisión - slippage =
YES_bid - costos; se incluyen solo las que aportan algo positivo, con k >= 2.

Cancelaciones: si el evento se cancela y cada pata liquida "scalar" a valores
que suman <= 1, k patas NO pagan k - sum(valores) >= k - 1. Sigue valiendo.

Solo lectura/paper: no envía órdenes.
"""

from dataclasses import replace

from .kalshi_common import (
    asks_for, evaluate_bundle, fee_coefficient_for, leg_is_tradable, top_yes_bid,
)
from ..event_arbitrage import _num, taker_fee

STRATEGY = "buy_all_no"
NEAR_MISS_GROSS = -0.03   # mismo criterio que kalshi_current: costo < 1.03 x pago


def leg_contribution(yes_bid, coef, slippage):
    """Aporte por contrato de una pata NO al top of book.

    Conservador: comisión de 1 contrato redondeada al centavo, como cobra
    Kalshi. Sin redondeo, una pata con YES bid 0.001 parecía aportar (+0.0009)
    y en realidad resta (0.001 - 0.01).
    """
    no_ask = 1.0 - yes_bid
    return yes_bid - taker_fee([(no_ask, 1.0)], coef) - slippage


def select_legs(markets, coef, slippage):
    """Subconjunto óptimo con precios del top of book: patas con aporte > 0."""
    scored = [(leg_contribution(top_yes_bid(m), coef, slippage), m)
              for m in markets if 0 < top_yes_bid(m) < 1]
    chosen = [m for c, m in sorted(scored, key=lambda x: -x[0]) if c > 0]
    return chosen


def prefilter(event, *, min_volume_24h=0.0, slippage=0.0, base_fee=0.07):
    """Filtro sin orderbooks. Devuelve (candidato | None, motivo).

    candidato = {"event", "legs", "gross_top", "coef"}
    """
    if not event.get("mutually_exclusive"):
        return None, "NOT_MUTUALLY_EXCLUSIVE"
    markets = event.get("markets") or []
    if any(m.get("market_type", "binary") != "binary" for m in markets):
        return None, "NON_BINARY_MARKET"
    if any((m.get("result") or "").lower() == "yes" for m in markets):
        return None, "ALREADY_DETERMINED"
    open_legs = [m for m in markets if leg_is_tradable(m)]
    if len(open_legs) < 2:
        return None, "LESS_THAN_2_OPEN_LEGS"
    volume = sum(_num(m.get("volume_24h_fp")) for m in open_legs)
    if volume < min_volume_24h:
        return None, "LOW_VOLUME"
    coef = fee_coefficient_for(event, base_fee)
    legs = select_legs(open_legs, coef, slippage)
    if len(legs) < 2:
        return None, "LESS_THAN_2_LEGS_WITH_BID"
    gross_top = sum(top_yes_bid(m) for m in legs) - 1.0
    if gross_top <= NEAR_MISS_GROSS:
        return None, "PRELIM_GROSS_TOO_LOW"
    return {"event": event, "legs": legs, "gross_top": gross_top, "coef": coef}, "OK"


def evaluate(candidate, books, *, slippage=0.0, min_net_edge=0.0,
             budget_usd=float("inf")):
    """Evalúa con orderbooks reales. Recalcula el subconjunto con los libros."""
    event = candidate["event"]
    coef = candidate["coef"]
    legs = []
    for m in candidate["legs"]:
        ladder = asks_for(books[m["ticker"]], "no")
        if ladder and leg_contribution(1.0 - ladder[0][0], coef, slippage) > 0:
            legs.append((m["ticker"], ladder))
    k = len(legs)
    tickers = [t for t, _ in legs] or [m["ticker"] for m in candidate["legs"]]
    ladders = [l for _, l in legs] or [asks_for(books[t], "no") for t in tickers]
    return evaluate_bundle(
        strategy=STRATEGY, event_ticker=event.get("event_ticker", ""),
        key=event.get("event_ticker", ""), tickers=tickers, sides=["no"] * len(tickers),
        ladders=ladders, min_payout_per_bundle=max(len(tickers) - 1, 0),
        fee_coefficient=coef, slippage_per_contract=slippage,
        min_net_edge=min_net_edge, budget_usd=budget_usd,
        extra={"k": k, "event_legs": len(event.get("markets") or []),
               "gross_top_prefilter": round(candidate["gross_top"], 4)},
    ) if k >= 2 else _too_few_legs(event, tickers, ladders, coef, slippage)


def _too_few_legs(event, tickers, ladders, coef, slippage):
    r = evaluate_bundle(
        strategy=STRATEGY, event_ticker=event.get("event_ticker", ""),
        key=event.get("event_ticker", ""), tickers=tickers,
        sides=["no"] * len(tickers), ladders=ladders,
        min_payout_per_bundle=max(len(tickers) - 1, 0), fee_coefficient=coef,
        slippage_per_contract=slippage)
    return replace(r, contracts=0, executable=False,
                   reason="LESS_THAN_2_LEGS_IN_BOOK")
