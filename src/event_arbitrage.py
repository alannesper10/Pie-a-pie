"""Arbitraje intra-evento: comprar YES en todos los resultados de un evento
mutuamente excluyente y exhaustivo. Exactamente una pata paga 1.00 USD, así que
si la suma de los YES ask (más comisiones y slippage) es < 1.00 hay ganancia.

Solo análisis: este módulo no envía órdenes.
"""

import math
import re
from dataclasses import dataclass, field, replace
from typing import List, Optional, Tuple

TRADABLE_STATUSES = {"active", "open"}

_LOWER_TYPES = {"less", "less_or_equal"}
_UPPER_TYPES = {"greater", "greater_or_equal"}

# Solo cuentan los mercados que cubren el resultado "nulo". Un "Other"/"Field"
# cubre otros ganadores, pero no "nadie lo logra antes de la fecha límite"
# (ej. KXMODELHIGH: 8 patas con "Other" sumaban 0.42 en YES ask).
_CATCH_ALL = re.compile(
    r"^(none|none of the above|no one|nobody|no winner|tie|draw)$"
)


def _num(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _norm(text):
    return re.sub(r"[^a-z0-9 ]+", "", (text or "").lower()).strip()


def is_catch_all(market):
    return any(
        _CATCH_ALL.match(_norm(market.get(k)))
        for k in ("yes_sub_title", "subtitle")
    )


def strikes_cover_real_line(markets, gap_tol=0.0):
    """True si los rangos (floor/cap) de los mercados cubren (-inf, +inf)."""
    intervals = []
    for m in markets:
        st = m.get("strike_type")
        floor, cap = m.get("floor_strike"), m.get("cap_strike")
        if st in _LOWER_TYPES and cap is not None:
            intervals.append((-math.inf, float(cap)))
        elif st in _UPPER_TYPES and floor is not None:
            intervals.append((float(floor), math.inf))
        elif st == "between" and floor is not None and cap is not None:
            intervals.append((float(floor), float(cap)))
        else:
            return False
    if not intervals:
        return False
    intervals.sort()
    if intervals[0][0] != -math.inf:
        return False
    reach = intervals[0][1]
    for lo, hi in intervals[1:]:
        if lo > reach + gap_tol:
            return False
        reach = max(reach, hi)
    return reach == math.inf


def check_exhaustive(event, gap_tol=0.0) -> Tuple[bool, str]:
    """Kalshi no expone un flag de exhaustividad; se confirma por estructura."""
    markets = event.get("markets") or []
    if is_catch_all_present(markets):
        return True, "CATCH_ALL_MARKET"
    if strikes_cover_real_line(markets, gap_tol):
        return True, "STRIKES_COVER_RANGE"
    return False, "EXHAUSTIVENESS_UNCONFIRMED"


def is_catch_all_present(markets):
    return any(is_catch_all(m) for m in markets)


@dataclass
class Prefiltered:
    event_ticker: str
    title: str
    legs: List[dict]
    prelim_sum: float
    volume_24h: float
    exhaustive_reason: str
    fee_multiplier: Optional[float]


LEG_FIELDS = ("ticker", "yes_sub_title", "status", "close_time",
              "expected_expiration_time", "yes_ask_dollars", "yes_ask_size_fp",
              "volume_24h_fp")


def prefilter_event(event, *, min_volume_24h=0.0, min_leg_ask_size=0.0,
                    max_prelim_sum=1.0, gap_tol=0.0, check_prices=True):
    """Filtro barato con los datos anidados de GET /events (sin orderbooks).

    Con check_prices=False solo aplica los filtros estructurales (excluyente,
    exhaustivo, patas abiertas, volumen), que son los que se pueden cachear:
    los precios se verifican después con orderbooks frescos.

    Devuelve (Prefiltered | None, motivo).
    """
    if not event.get("mutually_exclusive"):
        return None, "NOT_MUTUALLY_EXCLUSIVE"

    markets = event.get("markets") or []
    if len(markets) < 2:
        return None, "LESS_THAN_2_MARKETS"
    if any(m.get("market_type", "binary") != "binary" for m in markets):
        return None, "NON_BINARY_MARKET"

    legs = []
    for m in markets:
        result = (m.get("result") or "").lower()
        if result == "yes":
            return None, "ALREADY_DETERMINED"
        if result == "no":
            continue  # ya resolvió NO: no puede ser el ganador
        if m.get("status") not in TRADABLE_STATUSES:
            return None, "LEG_NOT_TRADABLE"
        legs.append(m)
    if len(legs) < 2:
        return None, "LESS_THAN_2_OPEN_LEGS"

    ok, reason = check_exhaustive(event, gap_tol)
    if not ok:
        return None, reason

    volume = sum(_num(m.get("volume_24h_fp")) for m in legs)
    if volume < min_volume_24h:
        return None, "LOW_VOLUME"

    prelim = 0.0
    for m in legs:
        ask = _num(m.get("yes_ask_dollars"))
        size = m.get("yes_ask_size_fp")
        if not check_prices:
            prelim += ask if 0 < ask < 1 else 1.0  # sin ask: al fondo del ranking
            continue
        if not 0 < ask < 1:
            return None, "LEG_WITHOUT_ASK"
        if size is not None and _num(size) < min_leg_ask_size:
            return None, "LEG_ASK_TOO_THIN"
        prelim += ask
    if check_prices and prelim > max_prelim_sum:
        return None, "PRELIM_SUM_TOO_HIGH"

    mult = event.get("fee_multiplier_override")
    return Prefiltered(
        event_ticker=event.get("event_ticker", ""),
        title=event.get("title", ""),
        legs=[{k: m.get(k) for k in LEG_FIELDS} for m in legs],
        prelim_sum=prelim,
        volume_24h=volume,
        exhaustive_reason=reason,
        fee_multiplier=_num(mult, None) if mult is not None else None,
    ), "OK"


def yes_asks_from_orderbook(data):
    """El libro solo trae bids: YES ask = 1 - NO bid, mismo tamaño.

    Devuelve [(precio_usd, cantidad)] ordenado del más barato al más caro.
    """
    book = data.get("orderbook_fp")
    if book is not None:
        no_bids = [(_num(p), _num(q)) for p, q in (book.get("no_dollars") or [])]
    else:  # formato viejo en centavos
        book = data.get("orderbook") or {}
        no_bids = [(_num(p) / 100.0, _num(q)) for p, q in (book.get("no") or [])]
    asks = [(round(1.0 - p, 6), q) for p, q in no_bids if 0 < p < 1 and q > 0]
    return sorted(asks)


def take_from_ladder(ladder, qty):
    """Fills para comprar `qty` contratos barriendo el ladder; None si no alcanza."""
    fills, need = [], qty
    for price, avail in ladder:
        if need <= 1e-9:
            break
        q = min(avail, need)
        fills.append((price, q))
        need -= q
    return fills if need <= 1e-9 else None


def taker_fee(fills, coefficient):
    """Comisión de una orden taker, redondeada hacia arriba al centavo."""
    raw = sum(coefficient * q * p * (1 - p) for p, q in fills)
    return math.ceil(round(raw * 100, 9)) / 100.0


@dataclass(frozen=True)
class EventOpportunity:
    event_ticker: str
    title: str
    n_legs: int
    best_ask_sum: float
    contracts: int
    max_contracts_available: float
    pair_cost: float                  # costo promedio por paquete (1 contrato por pata)
    gross_profit_per_contract: float
    estimated_fees: float             # total
    estimated_slippage: float         # total
    net_profit: float
    net_profit_per_contract: float
    net_return: float
    executable: bool
    reason: str
    exhaustive_reason: str
    legs: Tuple[Tuple[str, float, float], ...] = field(default=())  # (ticker, best_ask, size)


def evaluate_event_bundle(
    pre: Prefiltered,
    ladders: List[List[Tuple[float, float]]],
    *,
    fee_coefficient=0.07,
    slippage_per_contract=0.0,
    min_net_edge=0.0,
    budget_usd=math.inf,
    min_sane_ask_sum=0.0,
) -> EventOpportunity:
    n = len(ladders)
    tickers = [m.get("ticker", "") for m in pre.legs]
    coef = fee_coefficient * max(1.0, pre.fee_multiplier or 1.0)  # conservador

    def result(contracts, avail, cost, fees, slip, reason_override=None):
        best_sum = sum(l[0][0] for l in ladders) if all(ladders) else math.nan
        legs = tuple(
            (t, l[0][0] if l else math.nan, l[0][1] if l else 0.0)
            for t, l in zip(tickers, ladders)
        )
        gross = contracts - cost
        net = gross - fees - slip
        per = net / contracts if contracts else 0.0
        pair = cost / contracts if contracts else best_sum
        ret = net / cost if cost else 0.0
        executable = (reason_override is None and contracts >= 1
                      and net > 1e-12 and ret >= min_net_edge)
        reason = reason_override or ("NET_EDGE_OK" if executable
                                     else "INSUFFICIENT_NET_EDGE")
        return EventOpportunity(
            event_ticker=pre.event_ticker, title=pre.title, n_legs=n,
            best_ask_sum=best_sum, contracts=contracts,
            max_contracts_available=avail, pair_cost=pair,
            gross_profit_per_contract=(gross / contracts if contracts
                                       else 1.0 - best_sum),
            estimated_fees=fees, estimated_slippage=slip, net_profit=net,
            net_profit_per_contract=per, net_return=ret,
            executable=executable, reason=reason,
            exhaustive_reason=pre.exhaustive_reason, legs=legs,
        )

    if n < 2 or not all(ladders):
        return result(0, 0.0, 0.0, 0.0, 0.0, "EMPTY_BOOK_ON_SOME_LEG")

    # Barrido por niveles mientras el paquete marginal siga teniendo edge neto.
    idx = [0] * n
    rem = [l[0][1] for l in ladders]
    avail = 0.0
    while all(i < len(l) for i, l in zip(idx, ladders)):
        prices = [ladders[k][idx[k]][0] for k in range(n)]
        bundle = sum(prices)
        marginal = (1.0 - bundle - n * slippage_per_contract
                    - sum(coef * p * (1 - p) for p in prices))
        if marginal <= 0 or marginal / bundle < min_net_edge:
            break
        q = min(rem)
        avail += q
        for k in range(n):
            rem[k] -= q
            if rem[k] <= 1e-9:
                idx[k] += 1
                if idx[k] < len(ladders[k]):
                    rem[k] = ladders[k][idx[k]][1]

    if avail < 1:
        # Sin edge marginal: se reportan las cifras de 1 paquete al top of
        # book como referencia, pero con 0 contratos y no ejecutable.
        fills = [[(l[0][0], 1.0)] for l in ladders]
        ref = result(1, avail, sum(l[0][0] for l in ladders),
                     sum(taker_fee(f, coef) for f in fills),
                     n * slippage_per_contract)
        return replace(ref, contracts=0, executable=False,
                       reason="NO_POSITIVE_MARGINAL_EDGE")

    contracts = int(avail)
    while contracts >= 1:
        fills = [take_from_ladder(l, contracts) for l in ladders]
        cost = sum(p * q for f in fills for p, q in f)
        if cost <= budget_usd:
            break
        contracts = min(contracts - 1, int(budget_usd / (cost / contracts)))
    if contracts < 1:
        return result(0, avail, 0.0, 0.0, 0.0, "BUDGET_TOO_SMALL")

    fees = sum(taker_fee(f, coef) for f in fills)
    slip = contracts * n * slippage_per_contract
    opp = result(contracts, avail, cost, fees, slip)
    if opp.best_ask_sum < min_sane_ask_sum:
        # Un edge así de grande casi seguro indica un resultado no cubierto.
        return replace(opp, executable=False,
                       reason="SUSPICIOUS_EDGE_CHECK_RULES")
    return opp
