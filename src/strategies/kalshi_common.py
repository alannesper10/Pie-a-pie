"""Piezas comunes de las estrategias Kalshi nuevas (buy_all_no,
strike_inconsistency). kalshi_current NO usa este módulo: sigue en
scanner.py + src/event_arbitrage.py sin cambios.

Solo lectura y paper trading: nada acá envía órdenes.
"""

import math
import time
from datetime import datetime, timezone
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
        raw = client.get_orderbook(t, timeout=min(request_timeout_s, remaining))
        b = parse_book(raw)
        # Evidencia T0: libro crudo y hora exacta de la consulta.
        b["_raw"] = raw
        b["_fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        books[t] = b
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



# --------------------------------------- entradas repetidas (opt-in por estrategia) ---

ENTRY_FIELDS = [
    "timestamp", "entry_id", "strategy", "key", "event_ticker", "legs", "sides", "prices",
    "contracts", "cost", "fees", "slippage", "outlay", "min_payout", "expected_net",
    "expected_return_pct", "expected_close", "days_to_close", "annualized_return_pct",
    "lock_cost_usd", "excess_vs_reference_usd", "entries_open_for_key", "key_outlay_after",
    "cash_before", "cash_after", "case", "recovery_days", "recovery_at",
    "required_return_pct", "authorization_id",
]
DECISION_FIELDS = [
    "timestamp", "strategy", "key", "event_ticker", "decision", "reason", "case", "entry_id",
    "contracts", "outlay", "expected_net", "expected_return_pct", "recovery_days",
    "required_return_pct", "request_id", "new_request", "material_change",
    "entries_open_for_key", "key_outlay", "available_contracts", "cash_after", "ledger_gap",
]
AUTH_REQUEST_FIELDS = [
    "timestamp", "request_id", "replaces", "material_change", "strategy", "key", "event_ticker",
    "case", "reason", "legs", "sides", "prices", "contracts", "cost", "fees", "slippage", "outlay",
    "expected_net", "expected_return_pct", "recovery_days", "recovery_at", "recovery_basis",
    "required_return_pct", "shortfall_pp",
]


def entry_id_for(strategy, key, ts):
    """Determinístico por (estrategia, par, ciclo): reprocesar el mismo ciclo da
    el mismo id y el libro lo rechaza (DUPLICATE_ENTRY); un ciclo nuevo, con
    libros nuevos, es una evaluación de mercado distinta."""
    import hashlib
    return hashlib.sha1(f"{strategy}|{key}|{ts}".encode()).hexdigest()[:16]


def _days_to(expected_close, ts):
    try:
        a = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        b = datetime.fromisoformat(str(expected_close).replace("Z", "+00:00"))
        return max((b - a).total_seconds() / 86400, 0.0)
    except (TypeError, ValueError):
        return None


def time_adjusted(outlay, expected_net, expected_close, ts, reference_rate):
    """Rendimiento esperado, plazo y costo de inmovilizar el capital (informativo:
    no filtra). reference_rate: tasa anual de referencia (SUPUESTO)."""
    days = _days_to(expected_close, ts)
    ret = expected_net / outlay if outlay else 0.0
    if not days:
        return {"expected_return_pct": ret * 100, "days_to_close": days,
                "annualized_return_pct": None, "lock_cost_usd": None, "excess_vs_reference_usd": None}
    ann = ((1 + ret) ** (365 / days) - 1) * 100 if ret > -1 else None
    lock = outlay * reference_rate * days / 365
    return {"expected_return_pct": ret * 100, "days_to_close": round(days, 1),
            "annualized_return_pct": ann, "lock_cost_usd": lock,
            "excess_vs_reference_usd": expected_net - lock}


def _scale(r: BundleResult, n: int) -> BundleResult:
    """Reduce un paquete a n contratos. Proporcional al costo medio: conservador,
    porque menos contratos barren niveles más baratos del libro."""
    from dataclasses import replace
    f = n / r.contracts
    cost, fees, slip = r.cost * f, r.estimated_fees * f, r.estimated_slippage * f
    payout = n * r.min_payout_per_bundle
    net = payout - cost - fees - slip
    return replace(r, contracts=n, cost=cost, estimated_fees=fees, estimated_slippage=slip,
                   min_payout=payout, gross_profit=payout - cost, net_profit=net,
                   net_profit_per_contract=net / n, net_return=net / cost if cost else 0.0)


def open_paper_repeat(store, r: BundleResult, expected_close, ts, *, starting_cash,
                      max_key_outlay, reference_rate, markets=None, approvals=None):
    """Nueva entrada independiente sobre un par aunque ya haya posiciones abiertas.

    Controles técnicos (caso C si fallan), en orden:
      1. entrada no duplicada (reproceso del mismo ciclo)
      2. ledger reconciliado (caja + bloqueado − realizado = capital inicial)
      3. liquidez: se descuentan los contratos que nuestras entradas abiertas ya
         tomaron mientras el mejor ask de cada pata siga igual (en paper, ese libro
         "ya lo compramos"; las posiciones previas sin precios cuentan siempre)
      4. tope de capital por par (max_key_outlay)
      5. caja disponible
    Después, rentabilidad mínima por plazo de recupero (entry_gate): A abre,
    B y D piden autorización (approvals: las que escribió el usuario).
    Registra cada decisión en decisions.csv, cada entrada en entries.csv y
    paper_trades.csv (mismo formato de siempre) y cada solicitud nueva en
    authorization_requests.csv."""
    import math
    from . import entry_gate as eg
    eid = entry_id_for(store.strategy, r.key, ts)
    held = store.book.open_for_key(r.key, r.event_ticker)
    key_outlay = sum(p.outlay for p in held)
    prices = [round(p, 4) for _, p, _ in r.legs]
    consumed = sum(p.contracts for p in held
                   if p.entry_prices is None or [round(x, 4) for x in p.entry_prices] == prices)
    available = math.floor(r.max_contracts_available - consumed + 1e-9)
    gap = store.book.reconcile(starting_cash)
    reqs = eg.PendingRequests(store.dir / "authorization_requests.json")
    approvals = {**reqs.approved(), **(approvals or {})}   # celular + config/authorizations.json

    def log(row):
        store.log("authorization_events.csv", eg.EVENT_FIELDS, row)
    dec = {"timestamp": ts, "strategy": store.strategy, "key": r.key, "event_ticker": r.event_ticker,
           "entry_id": "", "contracts": 0, "outlay": 0.0, "expected_net": 0.0, "new_request": 0,
           "entries_open_for_key": len(held), "key_outlay": round(key_outlay, 4),
           "available_contracts": available, "ledger_gap": round(gap, 6)}

    def finish(decision, reason, case, pos=None):
        dec.update(decision=decision, reason=reason, case=case, cash_after=round(store.book.cash, 4))
        store.log("decisions.csv", DECISION_FIELDS, dec)
        return pos, reason

    def technical(reason):
        # caso C: cambió el estado de la oportunidad, la solicitud vigente deja de valer
        if eg.drop_pending(reqs, r.key, log, ts, reason):
            reqs.save()
        return finish("REJECTED", reason, "C")

    if store.book.has_entry(eid):
        return finish("REJECTED", "DUPLICATE_ENTRY", "C")       # reproceso: no toca solicitudes
    if abs(gap) > 1e-6:
        return technical("LEDGER_MISMATCH")
    per_contract = (r.cost + r.estimated_fees + r.estimated_slippage) / r.contracts
    n = min(r.contracts, available,
            math.floor((max_key_outlay - key_outlay) / per_contract + 1e-9) if per_contract > 0 else 0)
    if n < 1:
        return technical("LIQUIDITY_ALREADY_TAKEN" if available < 1 else "KEY_LIMIT")
    rr = r if n == r.contracts else _scale(r, n)
    outlay = rr.cost + rr.estimated_fees + rr.estimated_slippage
    if outlay > store.book.cash + 1e-9:
        return technical("INSUFFICIENT_CASH")

    ret_pct = rr.net_profit / outlay * 100 if outlay else 0.0
    days, recovery_at, basis = eg.recovery_period(markets, ts)
    case, reason, req = eg.classify(ret_pct, days)
    dec.update(contracts=n, outlay=round(outlay, 4), expected_net=round(rr.net_profit, 4),
               expected_return_pct=round(ret_pct, 4),
               recovery_days=round(days, 2) if days is not None else "",
               required_return_pct=req if req is not None else "")
    if case == "C":                       # muy lejos del mínimo: no se pide autorización
        return technical(reason)
    auth_id = ""
    if case in ("B", "D"):
        snap = {"case": case, "prices": prices, "return_pct": ret_pct, "days": days, "contracts": n}
        cur = reqs.pending.get(r.key)
        changes = eg.material_changes(cur["snapshot"], snap) if cur else []
        prev = cur
        rej = reqs.rejected.get(r.key)
        if cur is None and rej:
            changes = eg.material_changes(rej["snapshot"], snap)
            if not changes:                     # misma condición que el usuario rechazó
                dec["request_id"] = rej["request_id"]
                return finish("REJECTED_BY_USER", reason, case)
            reqs.rejected.pop(r.key)            # oportunidad materialmente distinta: se vuelve a pedir
            prev = {"request_id": rej["request_id"]}
        if prev is None or changes:
            rid = eg.request_id_for(store.strategy, r.key, ts)
            if cur is not None:
                info = reqs.decisions.get(cur["request_id"])
                if info and info.get("status") == "APPROVED":
                    info["status"] = "SUPERSEDED"
                    log(eg.event_row(ts, cur["request_id"], "CONDITIONS_CHANGED", r.key,
                                     f"{';'.join(changes)} -> nueva solicitud {rid}"))
            reqs.pending[r.key] = {"request_id": rid, "since": ts, "snapshot": snap}
            reqs.save()
            dec.update(request_id=rid, new_request=1, material_change=";".join(changes))
            store.log("authorization_requests.csv", AUTH_REQUEST_FIELDS, {
                "timestamp": ts, "request_id": rid, "replaces": prev["request_id"] if prev else "",
                "material_change": ";".join(changes), "strategy": store.strategy, "key": r.key,
                "event_ticker": r.event_ticker, "case": case, "reason": reason,
                "legs": ";".join(t for t, _, _ in r.legs), "sides": ";".join(r.sides),
                "prices": ";".join(f"{x:.4f}" for x in prices), "contracts": n,
                "cost": round(rr.cost, 4), "fees": round(rr.estimated_fees, 4),
                "slippage": round(rr.estimated_slippage, 4), "outlay": round(outlay, 4),
                "expected_net": round(rr.net_profit, 4), "expected_return_pct": round(ret_pct, 4),
                "recovery_days": round(days, 2) if days is not None else "",
                "recovery_at": recovery_at or "", "recovery_basis": basis,
                "required_return_pct": req if req is not None else "",
                "shortfall_pp": round(req - ret_pct, 4) if req is not None else "",
            })
            return finish("AUTHORIZATION_REQUIRED", reason, case)
        rid = cur["request_id"]
        dec["request_id"] = rid
        if rid not in (approvals or {}) or rid in reqs.used:
            return finish("AUTHORIZATION_REQUIRED", reason, case)
        auth_id = rid
        n = min(n, cur["snapshot"]["contracts"])                 # nunca más de lo autorizado
        if n != rr.contracts:
            rr = _scale(rr, n)
    else:                                                         # pasó a cumplir: la solicitud caduca
        changed = eg.drop_pending(reqs, r.key, log, ts, "ya cumple el mínimo")
        if reqs.rejected.pop(r.key, None) is not None or changed:
            reqs.save()

    cash_before = store.book.cash
    pos, why = store.book.try_open(rr, expected_close, ts, allow_repeat=True, entry_id=eid,
                                   key=r.key, entry_prices=prices)
    if not pos:
        return finish("REJECTED", why, "C")
    if auth_id:
        reqs.used.append(auth_id)
        reqs.pending.pop(r.key, None)
        if auth_id in reqs.decisions:
            reqs.decisions[auth_id]["status"] = "EXECUTED"
            log(eg.event_row(ts, auth_id, "EXECUTED", r.key, eid))
        reqs.save()
    tm = time_adjusted(pos.outlay, pos.expected_net, expected_close, ts, reference_rate)
    store.log("paper_trades.csv", PAPER_FIELDS, {
        "timestamp": ts, "action": "OPEN", "strategy": store.strategy,
        "event_ticker": pos.event_ticker, "legs": ";".join(pos.legs),
        "sides": ";".join(pos.sides or []), "contracts": pos.contracts,
        "cost": pos.cost, "fees": pos.fees, "slippage": pos.slippage,
        "min_payout": rr.min_payout, "expected_net": pos.expected_net,
        "cash_after": store.book.cash,
    })
    store.log("entries.csv", ENTRY_FIELDS, {
        "timestamp": ts, "entry_id": eid, "strategy": store.strategy, "key": r.key,
        "event_ticker": pos.event_ticker, "legs": ";".join(pos.legs), "sides": ";".join(pos.sides or []),
        "prices": ";".join(f"{x:.4f}" for x in prices), "contracts": pos.contracts,
        "cost": round(pos.cost, 4), "fees": round(pos.fees, 4), "slippage": round(pos.slippage, 4),
        "outlay": round(pos.outlay, 4), "min_payout": round(rr.min_payout, 4),
        "expected_net": round(pos.expected_net, 4), "expected_close": expected_close,
        **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in tm.items()},
        "entries_open_for_key": len(held) + 1, "key_outlay_after": round(key_outlay + pos.outlay, 4),
        "cash_before": round(cash_before, 4), "cash_after": round(store.book.cash, 4),
        "case": case, "recovery_days": round(days, 2) if days is not None else "",
        "recovery_at": recovery_at or "", "required_return_pct": req if req is not None else "",
        "authorization_id": auth_id,
    })
    dec.update(entry_id=eid, contracts=pos.contracts, outlay=round(pos.outlay, 4),
               expected_net=round(pos.expected_net, 4),
               expected_return_pct=round(pos.expected_net / pos.outlay * 100, 4))
    if auth_id:
        return finish("OPENED", "AUTHORIZED", case, pos)
    return finish("OPENED", "NEW_ENTRY" if held else "FIRST_ENTRY", case, pos)
