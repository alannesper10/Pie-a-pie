"""Arbitraje spot entre exchanges: comprar en A (ask) y vender en B (bid).

Supuesto de inventario: hay USDT en A y el activo en B de antemano (no se
transfiere por operación). Cada par de exchanges lleva su inventario: cada
operación consume nocional del inventario prepuesto (capital / 2 por lado) y
la transferencia de rebalanceo (ASSUMED) se cobra SOLO en la operación que lo
agota, no prorrateada en todas. El capital comprometido es 2x el nocional.
"""

from datetime import datetime

from ..core import (
    ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity, make_rng, walk,
)
from ..fees import fee_cost, rebalance_cost, taker_fee
from .base import Module

SYMBOLS = ("BTC/USDT", "ETH/USDT", "SOL/USDT")
MAX_BOOK_SKEW_MS = 2000
MAX_PLAUSIBLE_SPREAD = 0.015


def _ms_between(a, b):
    try:
        return abs((datetime.fromisoformat(a) - datetime.fromisoformat(b)).total_seconds()) * 1000
    except (TypeError, ValueError):
        return float("inf")


def _within_limit(levels, limit, side):
    ok = (lambda p: p <= limit + 1e-12) if side == "buy" else (lambda p: p >= limit - 1e-12)
    return [(p, q) for p, q in levels if ok(p)]


class CrossExchange(Module):
    name = "cross_exchange"
    needs_crypto_books = True

    def __init__(self, symbols=SYMBOLS):
        self.symbols = symbols
        self.checked = 0
        self.inventory_used = {}     # (símbolo, A, B) -> nocional ya usado desde el último rebalanceo
        self.rebalances = 0

    def _needs_rebalance(self, key, notional, capacity):
        return self.inventory_used.get(key, 0.0) + notional > capacity + 1e-9

    def evaluate(self, snap, ctx):
        out = []
        for sym in self.symbols:
            base = sym.split("/")[0]
            venues = [v for v in sorted({k.split("|")[0] for k in snap.books})
                      if snap.book(v, sym)]
            for a in venues:
                for b in venues:
                    if a == b:
                        continue
                    self.checked += 1
                    o = self._evaluate_pair(snap, ctx, sym, base, a, b)
                    if o:
                        out.append(o)
        return out

    def _evaluate_pair(self, snap, ctx, sym, base, a, b):
        ba, bb = snap.book(a, sym), snap.book(b, sym)
        asks, bids = ba.get("asks") or [], bb.get("bids") or []
        if not asks or not bids or bids[0][0] <= asks[0][0]:
            return None                        # sin spread bruto observado
        ma, mb = snap.markets.get(snap.k(a, sym), {}), snap.markets.get(snap.k(b, sym), {})
        fa, _ = taker_fee(a, ma.get("taker_ref"))
        fb, _ = taker_fee(b, mb.get("taker_ref"))
        o = Opportunity(
            strategy=self.name, key=f"{sym}|{a}->{b}", tick=snap.tick, ts=snap.ts,
            venues=[a, b], instruments=[sym],
            observed={"ask_a": asks[0], "bid_b": bids[0],
                      "raw_spread_pct": (bids[0][0] - asks[0][0]) / asks[0][0],
                      "fetched_a": ba.get("fetched_at"), "fetched_b": bb.get("fetched_at"),
                      "fetch_ms": [ba.get("fetch_ms"), bb.get("fetch_ms")]},
            assumptions=["inventario ubicado de antemano en ambos exchanges",
                         "rebalanceo solo cuando el inventario se agota",
                         "comisiones taker de nivel base"])

        skew = _ms_between(ba.get("fetched_at"), bb.get("fetched_at"))
        o.observed["book_skew_ms"] = skew
        if skew > MAX_BOOK_SKEW_MS:
            o.reason = "STALE_BOOKS"
            return o
        # Plausibilidad: entre exchanges grandes, una diferencia así casi siempre
        # es un libro viejo o retiros/depósitos suspendidos (no transferible).
        if o.observed["raw_spread_pct"] > MAX_PLAUSIBLE_SPREAD:
            o.reason = "SUSPICIOUS_SPREAD_CHECK_TRANSFERS"
            return o

        # Profundidad: avanzar mientras el paquete marginal tenga neto > 0.
        cap_notional = ctx.ledger.capital * ctx.max_trade_fraction / 2
        qty = spent = 0.0
        ia = ib = 0
        ra, rb = asks[0][1], bids[0][1]
        while ia < len(asks) and ib < len(bids):
            pa, pb = asks[ia][0], bids[ib][0]
            if pb * (1 - fb) - pa * (1 + fa) <= 0:
                break
            q = min(ra, rb, (cap_notional - spent) / pa)
            if q <= 1e-12:
                break
            qty += q
            spent += q * pa
            ra -= q
            rb -= q
            if ra <= 1e-12:
                ia += 1
                ra = asks[ia][1] if ia < len(asks) else 0
            if rb <= 1e-12:
                ib += 1
                rb = bids[ib][1] if ib < len(bids) else 0
        o.stage = "ESTIMATED"
        if qty <= 0:
            # Referencia con el MISMO tamaño que una operación real (capital y
            # top of book), no 1 unidad del activo (en BTC serían US$80.000+).
            q = min(cap_notional / asks[0][0], asks[0][1], bids[0][1])
            o.reason = "NO_EDGE_AFTER_FEES"
            o.size, o.capital_usd = q, 2 * q * asks[0][0]
            o.gross_usd = q * (bids[0][0] - asks[0][0])
            o.costs = {"fee_compra_" + a: fee_cost(q * asks[0][0], a, ma.get("taker_ref")),
                       "fee_venta_" + b: fee_cost(q * bids[0][0], b, mb.get("taker_ref"))}
            return o
        _, cost_buy, fills_a = walk(asks, qty)
        _, rev_sell, fills_b = walk(bids, qty)
        o.size = qty
        o.gross_usd = rev_sell - cost_buy
        o.capital_usd = 2 * cost_buy
        o.costs = {"fee_compra_" + a: fee_cost(cost_buy, a, ma.get("taker_ref")),
                   "fee_venta_" + b: fee_cost(rev_sell, b, mb.get("taker_ref")),
                   "profundidad": Cost(0.0, VERIFIED, "incluida: precio promedio barrido")}
        inv_key = (sym, a, b)
        if self._needs_rebalance(inv_key, cost_buy, cap_notional):
            o.costs["rebalanceo"] = rebalance_cost(base)
        o.observed["inventory_used_before"] = self.inventory_used.get(inv_key, 0.0)
        o.observed["inventory_capacity"] = cap_notional
        o.observed["limit_buy"] = fills_a[-1][0]
        o.observed["limit_sell"] = fills_b[-1][0]
        for m, v in ((ma, a), (mb, b)):
            if (m.get("min_cost") or 0) > cost_buy or (m.get("min_amount") or 0) > qty:
                o.reason = f"MIN_SIZE_{v}"
                return o
        o.reason = "ESTIMATED_POSITIVE" if o.net_estimated_usd > 0 else "NET_NEGATIVE_AFTER_COSTS"
        return o

    def execute(self, o, snap, ctx):
        if o.reason != "ESTIMATED_POSITIVE":
            return
        if not ctx.ledger.can_commit(o.capital_usd):
            o.reason = "NO_CAPITAL"
            return
        a, b = o.venues
        sym = o.instruments[0]
        ba, bb = snap.book(a, sym, after=True), snap.book(b, sym, after=True)
        if not ba or not bb:
            o.reason = "NO_BOOK_AFTER_LATENCY"
            return
        rng = make_rng(ctx.seed, self.name, f"{snap.tick}:{o.key}")
        ma, mb = snap.markets.get(snap.k(a, sym), {}), snap.markets.get(snap.k(b, sym), {})
        fa, _ = taker_fee(a, ma.get("taker_ref"))
        fb, _ = taker_fee(b, mb.get("taker_ref"))
        asks = _within_limit(ctx.registry.available(a, sym, "asks", ba["asks"]),
                             o.observed["limit_buy"], "buy")
        bids = _within_limit(ctx.registry.available(b, sym, "bids", bb["bids"]),
                             o.observed["limit_sell"], "sell")
        qb, cb, fills_a = walk(asks, o.size)
        leg_failed = rng.random() < ctx.exec_cfg.leg_fail_prob
        qs, rs, fills_b = (0.0, 0.0, []) if leg_failed else walk(bids, o.size)
        ctx.registry.claim(a, sym, "asks", fills_a)
        ctx.registry.claim(b, sym, "bids", fills_b)

        matched = min(qb, qs)
        unwind = 0.0
        pen = ctx.exec_cfg.unwind_penalty
        if qb > matched:      # compramos de más en A: se vende al bid de A
            ex_q = qb - matched
            ref = ba["bids"][0][0] if ba["bids"] else (cb / qb)
            unwind += ex_q * (cb / qb - ref) + ex_q * ref * (fa + pen)
        if qs > matched:      # vendimos de más en B: se recompra al ask de B
            ex_q = qs - matched
            ref = bb["asks"][0][0] if bb["asks"] else (rs / qs)
            unwind += ex_q * (ref - rs / qs) + ex_q * ref * (fb + pen)
        avg_b = cb / qb if qb else 0.0
        avg_s = rs / qs if qs else 0.0
        fees = cb * fa + rs * fb
        inv_key, rebal = (sym, a, b), 0.0
        if matched > 0:
            notional = matched * avg_b
            if self._needs_rebalance(inv_key, notional, o.observed["inventory_capacity"]):
                rebal = rebalance_cost(sym.split("/")[0]).usd
                self.inventory_used[inv_key] = 0.0
                self.rebalances += 1
            self.inventory_used[inv_key] = self.inventory_used.get(inv_key, 0.0) + notional
        net = matched * (avg_s - avg_b) - fees - unwind - rebal
        ctx.ledger.commit(o.capital_usd)
        ctx.ledger.release(o.capital_usd, net, {"key": o.key, "tick": snap.tick})
        status = ("DISAPPEARED" if qb == 0 and qs == 0 else
                  "LEG_FAILED" if leg_failed else
                  "PARTIAL" if matched < o.size - 1e-12 else "FILLED")
        o.stage = "SIMULATED"
        o.sim = {"status": status, "filled_buy": qb, "filled_sell": qs, "matched": matched,
                 "fees_usd": fees, "unwind_usd": unwind, "rebalance_usd": rebal, "net_usd": net,
                 "net_pct_capital": net / o.capital_usd if o.capital_usd else 0.0,
                 "latency_ms": snap.latency_ms}
        o.decision = ACCEPTED if matched > 0 else REJECTED
        o.reason = status
