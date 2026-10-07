"""Piezas comunes de las estrategias Kalshi nuevas (buy_all_no,
strike_inconsistency). kalshi_current NO usa este módulo: sigue en
scanner.py + src/event_arbitrage.py sin cambios.

Solo lectura y paper trading: nada acá envía órdenes.
"""

import math
import time
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional, Tuple

from ..event_arbitrage import _num, take_from_ladder, taker_fee
from ..paper_trader import PaperBook
from ..tracking import StreakTracker, append_csv, load_json, save_json

TRADABLE_STATUSES = {"active", "open"}
SUSPICIOUS_GROSS_RETURN = 0.10   # ganancia bruta > 10% del costo => sospechosa


# ------------------------------------------------------------ orderbooks ---

def parse_book(data):
    """Devuelve {"yes_bids": [(p, q)], "no_bids": [(p, q)]} en USD, mejor primero.

    Kalshi solo publica bids: YES ask = 1 - NO bid y NO ask = 1 - YES bid.
    """
    book = data.get("orderbook_fp")
    if book is not None:
        yes = [(_num(p), _num(q)) for p, q in (book.get("yes_dollars") or [])]
        no = [(_num(p), _num(q)) for p, q in (book.get("no_dollars") or [])]
    else:  # formato viejo en centavos
        book = data.get("orderbook") or {}
        yes = [(_num(p) / 100, _num(q)) for p, q in (book.get("yes") or [])]
        no = [(_num(p) / 100, _num(q)) for p, q in (book.get("no") or [])]
    clean = lambda lv: sorted(((p, q) for p, q in lv if 0 < p < 1 and q > 0),  # noqa: E731
                              reverse=True)
    return {"yes_bids": clean(yes), "no_bids": clean(no)}


def asks_for(book, side):
    """Ladder de asks [(precio, cantidad)] para comprar `side` ("yes"/"no")."""
    opposite = book["no_bids"] if side == "yes" else book["yes_bids"]
    return sorted((round(1.0 - p, 6), q) for p, q in opposite)


def fetch_books(client, tickers, timeout_s, request_timeout_s=10.0):
    """Libros de varias patas con un deadline común (timeout por evento)."""
    deadline = time.monotonic() + timeout_s
    books = {}
    for t in tickers:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(t)
        books[t] = parse_book(client.get_orderbook(
            t, timeout=min(request_timeout_s, remaining)))
    return books


# -------------------------------------------------- evaluador de paquetes ---

@dataclass(frozen=True)
class BundleResult:
    """Paquete = 1 contrato por pata. Compatible con PaperBook.try_open."""
    strategy: str
    event_ticker: str
    key: str                      # identifica la oportunidad para rachas
    legs: Tuple[Tuple[str, float, float], ...]   # (ticker, mejor ask, tamaño)
    sides: Tuple[str, ...]
    min_payout_per_bundle: float
    contracts: int
    max_contracts_available: float
    pair_cost: float              # costo promedio por paquete
    cost: float                   # costo total
    min_payout: float             # total garantizado
    gross_profit: float
    estimated_fees: float
    estimated_slippage: float
    net_profit: float
    net_profit_per_contract: float
    net_return: float
    best_bundle_cost: float       # costo del paquete al top of book
    executable: bool
    reason: str
    extra: dict = field(default_factory=dict)


def evaluate_bundle(*, strategy, event_ticker, key, tickers, sides, ladders,
                    min_payout_per_bundle, fee_coefficient=0.07,
                    slippage_per_contract=0.0, min_net_edge=0.0,
                    budget_usd=math.inf, extra=None):
    """Compra 1 contrato por pata, barriendo profundidad mientras el paquete
    marginal tenga edge neto. Conservador: comisión taker redondeada hacia
    arriba al centavo por pata, slippage por contrato y por pata.

    Controles en orden: libro vacío, sin edge marginal, presupuesto
    (BUDGET_TOO_SMALL), plausibilidad (SUSPICIOUS_EDGE_CHECK_RULES), edge neto.
    """
    n = len(ladders)
    extra = extra or {}
    legs = tuple((t, l[0][0] if l else math.nan, l[0][1] if l else 0.0)
                 for t, l in zip(tickers, ladders))
    best_cost = sum(l[0][0] for l in ladders) if all(ladders) else math.nan

    def build(contracts, avail, cost, fees, slip, reason=None, executable=None):
        payout = contracts * min_payout_per_bundle
        gross = payout - cost
        net = gross - fees - slip
        ret = net / cost if cost else 0.0
        if executable is None:
            executable = (reason is None and contracts >= 1 and net > 1e-12
                          and ret >= min_net_edge)
        if reason is None:
            reason = "NET_EDGE_OK" if executable else "INSUFFICIENT_NET_EDGE"
        return BundleResult(
            strategy=strategy, event_ticker=event_ticker, key=key, legs=legs,
            sides=tuple(sides), min_payout_per_bundle=min_payout_per_bundle,
            contracts=contracts, max_contracts_available=avail,
            pair_cost=cost / contracts if contracts else best_cost,
            cost=cost, min_payout=payout, gross_profit=gross,
            estimated_fees=fees, estimated_slippage=slip, net_profit=net,
            net_profit_per_contract=net / contracts if contracts else 0.0,
            net_return=ret, best_bundle_cost=best_cost, executable=executable,
            reason=reason, extra=extra)

    if n < 1 or not all(ladders):
        return build(0, 0.0, 0.0, 0.0, 0.0, "EMPTY_BOOK_ON_SOME_LEG", False)

    # Referencia: 1 paquete al top of book (se reporta aunque no se opere).
    top_fills = [[(l[0][0], 1.0)] for l in ladders]
    ref = build(1, 0.0, best_cost, sum(taker_fee(f, fee_coefficient) for f in top_fills),
                n * slippage_per_contract)
    min_outlay = best_cost + ref.estimated_fees + ref.estimated_slippage
    extra["min_bundle_outlay"] = round(min_outlay, 4)
    extra["fits_budget"] = min_outlay <= budget_usd

    # Plausibilidad antes que nada: un edge enorme casi siempre es un error de
    # modelado (patas mal agrupadas, resultado no cubierto), no plata gratis.
    if best_cost > 0 and (min_payout_per_bundle - best_cost) / best_cost > SUSPICIOUS_GROSS_RETURN:
        return replace(ref, contracts=0, executable=False,
                       reason="SUSPICIOUS_EDGE_CHECK_RULES")

    idx, rem = [0] * n, [l[0][1] for l in ladders]
    avail = 0.0
    while all(i < len(l) for i, l in zip(idx, ladders)):
        prices = [ladders[k][idx[k]][0] for k in range(n)]
        bundle = sum(prices)
        marginal = (min_payout_per_bundle - bundle - n * slippage_per_contract
                    - sum(fee_coefficient * p * (1 - p) for p in prices))
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
        # avail > 0: el edge existe pero el libro no llega a 1 contrato (Kalshi
        # admite tamaños fraccionarios, ej. 0.13 en KXGOVTCUTS-28-1).
        return replace(ref, contracts=0, max_contracts_available=avail,
                       executable=False,
                       reason="INSUFFICIENT_DEPTH" if avail > 0
                       else "NO_POSITIVE_MARGINAL_EDGE")

    if min_outlay > budget_usd:
        return replace(ref, contracts=0, max_contracts_available=avail,
                       executable=False, reason="BUDGET_TOO_SMALL")

    contracts = int(avail)
    while contracts >= 1:
        fills = [take_from_ladder(l, contracts) for l in ladders]
        cost = sum(p * q for f in fills for p, q in f)
        fees = sum(taker_fee(f, fee_coefficient) for f in fills)
        slip = contracts * n * slippage_per_contract
        if cost + fees + slip <= budget_usd:
            break
        contracts -= 1
    if contracts < 1:
        return replace(ref, contracts=0, max_contracts_available=avail,
                       executable=False, reason="BUDGET_TOO_SMALL")
    return build(contracts, avail, cost, fees, slip)


def is_net_positive(r: BundleResult):
    """Neto > 0 después de todos los costos, con al menos 1 contrato disponible
    con edge y sin la marca de sospechoso. Puede no ser ejecutable (presupuesto)."""
    return (r.max_contracts_available >= 1 and r.net_profit > 0
            and r.reason != "SUSPICIOUS_EDGE_CHECK_RULES")


def fee_coefficient_for(event, base=0.07):
    """Mismo criterio conservador que kalshi_current con fee_multiplier_override."""
    mult = _num(event.get("fee_multiplier_override"), None)
    return base * max(1.0, mult or 1.0)


# ------------------------------------------------------------ almacenamiento ---

OPPORTUNITY_FIELDS = [
    "timestamp", "strategy", "event_ticker", "key", "n_legs", "legs", "sides",
    "prices", "sizes", "contracts", "max_contracts_available", "cost",
    "min_payout", "fees", "slippage", "gross_profit", "net_profit",
    "net_per_bundle", "best_bundle_cost", "executable", "reason", "detail",
]
DISCARD_FIELDS = ["timestamp", "strategy", "reason", "count"]
STRATEGY_CYCLE_FIELDS = [
    "timestamp", "strategy", "ok", "error", "events_seen", "candidates",
    "evaluated", "timeouts", "errors", "opportunities", "net_positive",
    "executable", "paper_opened", "paper_settled", "t_books_s", "t_total_s",
]
PAPER_FIELDS = [
    "timestamp", "action", "strategy", "event_ticker", "legs", "sides",
    "contracts", "cost", "fees", "slippage", "min_payout", "expected_net",
    "payout", "realized_net", "cash_after",
]


def opportunity_row(ts, r: BundleResult):
    return {
        "timestamp": ts, "strategy": r.strategy, "event_ticker": r.event_ticker,
        "key": r.key, "n_legs": len(r.legs),
        "legs": ";".join(t for t, _, _ in r.legs), "sides": ";".join(r.sides),
        "prices": ";".join(f"{p:.4f}" for _, p, _ in r.legs),
        "sizes": ";".join(f"{q:g}" for _, _, q in r.legs),
        "contracts": r.contracts,
        "max_contracts_available": round(r.max_contracts_available, 2),
        "cost": round(r.cost, 4), "min_payout": round(r.min_payout, 4),
        "fees": round(r.estimated_fees, 4), "slippage": round(r.estimated_slippage, 4),
        "gross_profit": round(r.gross_profit, 4), "net_profit": round(r.net_profit, 4),
        "net_per_bundle": round(r.net_profit_per_contract if r.contracts
                                else r.net_profit, 4),
        "best_bundle_cost": round(r.best_bundle_cost, 4),
        "executable": r.executable, "reason": r.reason,
        "detail": ";".join(f"{k}={v}" for k, v in sorted(r.extra.items())),
    }


class StrategyStore:
    """Estado y registros de UNA estrategia, en su propio directorio.

    Capital, posiciones, P&L y rachas no se comparten con ninguna otra.
    """

    def __init__(self, root, strategy, starting_cash, max_gap_min):
        self.strategy = strategy
        self.dir = Path(root) / strategy
        state = load_json(self.dir / "state.json", {}) or {}
        self.book = PaperBook.from_dict(state.get("paper"), starting_cash)
        self.tracker = StreakTracker(state.get("streaks"), max_gap_min=max_gap_min)

    def save(self):
        save_json(self.dir / "state.json",
                  {"paper": self.book.to_dict(), "streaks": self.tracker.active})

    def log(self, name, fields, row):
        append_csv(self.dir / name, fields, row)


def settle_open_positions(client, store, ts, log):
    """Liquida posiciones paper cuyos mercados ya están finalized."""
    settled, cache = 0, {}
    for pos in list(store.book.open):
        try:
            if pos.event_ticker not in cache:
                data = client.get(f"events/{pos.event_ticker}",
                                  params={"with_nested_markets": "true"})
                markets = ((data.get("event") or {}).get("markets")
                           or data.get("markets") or [])
                cache[pos.event_ticker] = {m.get("ticker"): m for m in markets}
        except Exception as e:  # noqa: BLE001
            log.warning("    [%s] no se pudo consultar %s: %s", store.strategy,
                        pos.event_ticker, e)
            continue
        if store.book.try_settle(pos, cache[pos.event_ticker], ts):
            settled += 1
            store.log("paper_trades.csv", PAPER_FIELDS, {
                "timestamp": ts, "action": "SETTLE", "strategy": store.strategy,
                "event_ticker": pos.event_ticker, "legs": ";".join(pos.legs),
                "sides": ";".join(pos.sides or []), "contracts": pos.contracts,
                "cost": pos.cost, "fees": pos.fees, "slippage": pos.slippage,
                "expected_net": pos.expected_net, "payout": pos.payout,
                "realized_net": pos.realized_net, "cash_after": store.book.cash,
            })
    return settled


def open_paper(store, r: BundleResult, expected_close, ts):
    pos, why = store.book.try_open(r, expected_close, ts)
    if pos:
        store.log("paper_trades.csv", PAPER_FIELDS, {
            "timestamp": ts, "action": "OPEN", "strategy": store.strategy,
            "event_ticker": pos.event_ticker, "legs": ";".join(pos.legs),
            "sides": ";".join(pos.sides or []), "contracts": pos.contracts,
            "cost": pos.cost, "fees": pos.fees, "slippage": pos.slippage,
            "min_payout": r.min_payout, "expected_net": pos.expected_net,
            "cash_after": store.book.cash,
        })
    return pos, why


def leg_is_tradable(m):
    return m.get("status") in TRADABLE_STATUSES and not m.get("result")


def expected_close(markets) -> Optional[str]:
    times = sorted(t for m in markets
                   for t in [m.get("expected_expiration_time") or m.get("close_time")] if t)
    return times[-1] if times else None


def top_yes_bid(m):
    return _num(m.get("yes_bid_dollars"))


def top_yes_ask(m):
    return _num(m.get("yes_ask_dollars"))

