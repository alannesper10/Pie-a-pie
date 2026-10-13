"""Arbitraje triangular dentro de un exchange: USDT -> X -> Y -> USDT.

Cada pata es una orden taker. Se barre la profundidad real; las comisiones se
cobran en cada pata. Al ejecutar (libro tras la latencia) lo que quede en un
activo intermedio se vende de vuelta a USDT con penalidad.
"""

from ..core import ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity, make_rng, walk, walk_quote
from ..fees import taker_fee
from .base import Module

ASSETS = ("BTC", "ETH", "SOL")
START = "USDT"
SIZES = (10.0, 25.0, 50.0)     # USDT de entrada a probar


def _market(snap, venue, frm, to, after=False):
    """Devuelve (símbolo, lado, libro) para convertir frm -> to, o None."""
    for sym, side in ((f"{to}/{frm}", "buy"), (f"{frm}/{to}", "sell")):
        b = snap.book(venue, sym, after)
        if b:
            return sym, side, b
    return None


def convert(amount, side, book, fee, levels=None):
    """Convierte `amount` por una pata. -> (recibido, fills, lado_libro)."""
    if side == "buy":     # gasto quote, recibo base
        lv = levels if levels is not None else book["asks"]
        got, spent, fills = walk_quote(lv, amount)
        return got * (1 - fee), fills, "asks", spent
    lv = levels if levels is not None else book["bids"]
    q, rev, fills = walk(lv, amount)
    return rev * (1 - fee), fills, "bids", q


class Triangular(Module):
    name = "triangular"
    needs_crypto_books = True

    def evaluate(self, snap, ctx):
        out = []
        venues = sorted({k.split("|")[0] for k in snap.books})
        for v in venues:
            for x in ASSETS:
                for y in ASSETS:
                    if x == y:
                        continue
                    path = [START, x, y, START]
                    legs = [_market(snap, v, path[i], path[i + 1]) for i in range(3)]
                    if any(l is None for l in legs):
                        continue
                    o = self._evaluate_path(snap, ctx, v, path, legs)
                    if o:
                        out.append(o)
        return out

    def _top_rate(self, legs):
        r = 1.0
        for sym, side, b in legs:
            if not b.get("asks") or not b.get("bids"):
                return None
            r = r / b["asks"][0][0] if side == "buy" else r * b["bids"][0][0]
        return r

    def _evaluate_path(self, snap, ctx, v, path, legs):
        raw = self._top_rate(legs)
        if raw is None or raw <= 1.0:
            return None                      # sin ganancia bruta observada
        fees = [taker_fee(v, snap.markets.get(snap.k(v, s), {}).get("taker_ref"))[0]
                for s, _, _ in legs]
        o = Opportunity(
            strategy=self.name, key=f"{v}|{'->'.join(path)}", tick=snap.tick, ts=snap.ts,
            venues=[v], instruments=[s for s, _, _ in legs],
            observed={"top_rate": raw, "raw_gross_pct": raw - 1,
                      "fetched": [b.get("fetched_at") for _, _, b in legs]},
            assumptions=["3 órdenes taker secuenciales", "comisión de nivel base en cada pata"],
            stage="ESTIMATED")
        best = None
        cap = ctx.ledger.capital * ctx.max_trade_fraction
        for size in (s for s in SIZES if s <= cap):
            amt, ok = size, True
            for (sym, side, b), f in zip(legs, fees):
                gross_out, fills, _, used = convert(amt, side, b, 0.0)
                if used < (amt - 1e-9 if side == "sell" else amt * 0.999):
                    ok = False               # no hay profundidad para este tamaño
                    break
                amt = gross_out * (1 - f)
            if not ok:
                continue
            net = amt - size
            if best is None or net > best[1]:
                best = (size, net, amt)
        if best is None:
            o.reason = "INSUFFICIENT_DEPTH"
            return o
        size, net, final = best
        o.size = o.capital_usd = size
        # Separación bruto / costos: fees en USD aproximadas por pata (fracción del monto).
        fee_pct_total = 1 - (1 - fees[0]) * (1 - fees[1]) * (1 - fees[2])
        fee_usd = size * fee_pct_total * raw
        o.gross_usd = net + fee_usd
        o.costs = {"fees_3_patas": Cost(fee_usd, ASSUMED, "comisiones taker de nivel base x3"),
                   "profundidad": Cost(0.0, VERIFIED, "incluida: precios promedio barridos")}
        o.observed["final_usdt_estimated"] = final
        o.reason = "ESTIMATED_POSITIVE" if o.net_estimated_usd > 0 else "NET_NEGATIVE_AFTER_COSTS"
        return o

    @staticmethod
    def _to_usdt(snap, v, asset, qty, ctx):
        """Valúa un remanente en USDT vendiéndolo al bid tras la latencia, con
        comisión y penalidad de deshacer (conservador)."""
        if qty <= 0:
            return 0.0
        if asset == START:
            return qty
        b = snap.book(v, f"{asset}/USDT", after=True) or snap.book(v, f"{asset}/USDT")
        px = b["bids"][0][0] if b and b.get("bids") else 0.0
        return qty * px * (1 - taker_fee(v)[0] - ctx.exec_cfg.unwind_penalty)

    def execute(self, o, snap, ctx):
        if o.reason != "ESTIMATED_POSITIVE":
            return
        if not ctx.ledger.can_commit(o.capital_usd):
            o.reason = "NO_CAPITAL"
            return
        v = o.venues[0]
        path = o.key.split("|")[1].split("->")
        rng = make_rng(ctx.seed, self.name, f"{snap.tick}:{o.key}")
        amt, holding = o.size, path[0]
        leftovers = []                      # (activo, cantidad) no convertida
        fees_total, status = 0.0, "FILLED"
        for i in range(3):
            m = _market(snap, v, path[i], path[i + 1], after=True)
            if m is None:
                status = "NO_BOOK_AFTER_LATENCY"
                break
            sym, side, b = m
            if i > 0 and rng.random() < ctx.exec_cfg.leg_fail_prob:
                status = "LEG_FAILED"
                break
            f = taker_fee(v, snap.markets.get(snap.k(v, sym), {}).get("taker_ref"))[0]
            book_side = "asks" if side == "buy" else "bids"
            lv = ctx.registry.available(v, sym, book_side, b[book_side])
            out, fills, _, used = convert(amt, side, b, f, levels=lv)
            ctx.registry.claim(v, sym, book_side, fills)
            fees_total += out / (1 - f) * f
            if out <= 0:
                status = "DISAPPEARED" if i == 0 else "LEG_FAILED"
                break
            if amt - used > (amt * 0.001 if side == "buy" else 1e-12):
                status = "PARTIAL"
                leftovers.append((holding, amt - used))
            amt, holding = out, path[i + 1]
        leftovers.append((holding, amt))
        final = sum(self._to_usdt(snap, v, a, q, ctx) for a, q in leftovers)
        net = final - o.size if status != "DISAPPEARED" else 0.0
        amt = final
        ctx.ledger.commit(o.capital_usd)
        ctx.ledger.release(o.capital_usd, net, {"key": o.key, "tick": snap.tick})
        o.stage = "SIMULATED"
        o.sim = {"status": status, "final_usdt": amt, "fees_usd": fees_total, "net_usd": net,
                 "net_pct_capital": net / o.capital_usd, "latency_ms": snap.latency_ms}
        o.decision = ACCEPTED if status in ("FILLED", "PARTIAL") else REJECTED
        o.reason = status
