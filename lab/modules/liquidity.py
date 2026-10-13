"""Provisión de liquidez con órdenes límite (simulada, conservadora).

Modelo de cola:
  * Cada tick se cancelan y reponen las órdenes al mejor bid/ask observado
    (unirse al nivel = quedar al FINAL de la cola visible).
  * La orden existe recién después de la latencia; trades anteriores no cuentan.
  * Un trade vendedor a nuestro precio primero consume la cola de adelante; uno
    a peor precio implica que nuestro nivel se barrió (fill completo).
  * Selección adversa: markout = movimiento del mid al tick siguiente.
Fuentes: libro + trades públicos (OBSERVED). Comisión maker ASSUMED. Sin
rebates (no verificados por cuenta).
"""

from ..core import ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity
from ..fees import maker_fee
from ..sources import MM_MARKETS
from .base import Module

QUOTE_USD = 10.0          # tamaño por lado, en USDT
MAX_INVENTORY_USD = 30.0  # tope de inventario neto


def _iso_ms(iso):
    from datetime import datetime
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


def apply_trades(order, trades, side):
    """Fill de una orden límite según la cola. Modifica `order`. -> cantidad llenada."""
    filled = 0.0
    for t in sorted(trades, key=lambda t: t["ts"]):
        if t["ts"] < order["active_from_ms"] or order["remaining"] <= 1e-12:
            continue
        hits_us = (t["side"] == "sell") if side == "bid" else (t["side"] == "buy")
        if not hits_us:
            continue
        p = t["price"]
        through = p < order["price"] - 1e-12 if side == "bid" else p > order["price"] + 1e-12
        at = abs(p - order["price"]) <= 1e-12
        if through:                         # el nivel se barrió entero
            q = order["remaining"]
        elif at:
            consume = t["amount"]
            if order["queue_ahead"] >= consume:
                order["queue_ahead"] -= consume
                continue
            q = min(order["remaining"], consume - order["queue_ahead"])
            order["queue_ahead"] = 0.0
        else:
            continue
        order["remaining"] -= q
        filled += q
    return filled


class LiquidityProvision(Module):
    name = "liquidity_provision"
    nature = "speculative"   # depende de fills futuros y selección adversa
    needs_crypto_books = True
    needs_trades = True

    def __init__(self, markets=MM_MARKETS):
        self.markets = markets
        self.state = {}     # mercado -> {"orders", "inv", "cash", "pending", "fills"}
        self.updated = []   # oportunidades ya guardadas que cambiaron (markout)

    def pop_updated(self):
        out, self.updated = self.updated, []
        return out

    def evaluate(self, snap, ctx):
        out = []
        for venue, sym in self.markets:
            k = snap.k(venue, sym)
            book = snap.books.get(k)
            st = self.state.setdefault(k, {"orders": {}, "inv": 0.0, "cash": 0.0,
                                           "pending": [], "fills": 0})
            if not book or not book.get("bids") or not book.get("asks"):
                continue
            mid = (book["bids"][0][0] + book["asks"][0][0]) / 2
            fee, _ = maker_fee(venue, snap.markets.get(k, {}).get("maker_ref"))
            trades = snap.trades.get(k)
            # 1) markouts de fills del tick anterior (selección adversa)
            self.updated.extend(st["pending"])
            for o in st["pending"]:
                o.sim["markout_usd"] = (mid - o.sim["fill_price"]) * o.sim["qty"] * (
                    1 if o.sim["side"] == "bid" else -1)
                o.sim["net_usd"] = o.sim["spread_usd"] - o.sim["fee_usd"] + o.sim["markout_usd"]
                o.sim["net_pct_capital"] = o.sim["net_usd"] / o.capital_usd
            st["pending"] = []
            # 2) fills de las órdenes vivas con los trades públicos
            if trades is None and st["orders"]:
                for side in st["orders"]:
                    out.append(self._record(snap, venue, sym, side, None, 0, mid, fee,
                                            reason="NO_TRADES_DATA"))
            for side, order in list(st["orders"].items()):
                q = apply_trades(order, trades or [], side)
                if q > 0:
                    o = self._record(snap, venue, sym, side, order, q, order["mid_at_quote"], fee)
                    st["inv"] += q if side == "bid" else -q
                    st["cash"] += (-q if side == "bid" else q) * order["price"] - q * order["price"] * fee
                    st["fills"] += 1
                    st["pending"].append(o)
                    out.append(o)
            # 3) reponer órdenes al mejor precio (al final de la cola)
            inv_usd = st["inv"] * mid
            st["orders"] = {}
            active = _iso_ms(snap.ts) + int(snap.latency_ms)
            for side, lv in (("bid", book["bids"][0]), ("ask", book["asks"][0])):
                if side == "bid" and inv_usd >= MAX_INVENTORY_USD:
                    continue
                if side == "ask" and inv_usd <= -MAX_INVENTORY_USD:
                    continue
                st["orders"][side] = {"price": lv[0], "queue_ahead": lv[1],
                                      "remaining": QUOTE_USD / lv[0], "qty": QUOTE_USD / lv[0],
                                      "active_from_ms": active, "mid_at_quote": mid}
        return out

    def _record(self, snap, venue, sym, side, order, q, mid, fee, reason=None):
        o = Opportunity(
            strategy=self.name, key=f"{venue}|{sym}|{side}", tick=snap.tick, ts=snap.ts,
            venues=[venue], instruments=[sym], stage="SIMULATED",
            observed={"order_price": order and order["price"], "mid_at_quote": mid,
                      "queue_ahead_at_quote": order and order.get("qty")},
            assumptions=["unirse al mejor nivel = final de la cola visible",
                         "cancelar/reponer cada tick (se pierde prioridad)",
                         "comisión maker de nivel base, sin rebates"],
            capital_usd=2 * QUOTE_USD)
        if reason:
            o.reason = reason
            return o
        notional = q * order["price"]
        spread = (mid - order["price"]) * q if side == "bid" else (order["price"] - mid) * q
        o.size = q
        o.gross_usd = spread
        o.costs = {"fee_maker": Cost(notional * fee, ASSUMED, "comisión maker de nivel base"),
                   "seleccion_adversa": Cost(0.0, VERIFIED, "se mide en el tick siguiente (markout)")}
        o.sim = {"status": "FILLED" if order["remaining"] <= 1e-12 else "PARTIAL",
                 "side": side, "qty": q, "fill_price": order["price"],
                 "spread_usd": spread, "fee_usd": notional * fee, "markout_usd": None,
                 "net_usd": None, "net_pct_capital": None}
        o.decision, o.reason = ACCEPTED, "FILL"
        return o

    def execute(self, o, snap, ctx):
        return None     # los fills se resuelven dentro de evaluate (estado entre ticks)

    def finalize(self, ctx, last_snap):
        """Cierra el inventario al mid final (mark-to-market) en el ledger."""
        pnl = 0.0
        for k, st in self.state.items():
            b = last_snap.books.get(k) if last_snap else None
            if not b or not b.get("bids") or not b.get("asks"):
                continue
            mid = (b["bids"][0][0] + b["asks"][0][0]) / 2
            self.updated.extend(st["pending"])
            for o in st["pending"]:          # markout de los últimos fills
                o.sim["markout_usd"] = (mid - o.sim["fill_price"]) * o.sim["qty"] * (
                    1 if o.sim["side"] == "bid" else -1)
                o.sim["net_usd"] = o.sim["spread_usd"] - o.sim["fee_usd"] + o.sim["markout_usd"]
                o.sim["net_pct_capital"] = o.sim["net_usd"] / o.capital_usd
            st["pending"] = []
            pnl += st["cash"] + st["inv"] * mid      # inventario a mercado
        committed = min(2 * QUOTE_USD * len(self.markets), ctx.ledger.cash)
        ctx.ledger.commit(committed)
        ctx.ledger.release(committed, pnl, {"key": "mark_to_market_final"})
        return pnl
