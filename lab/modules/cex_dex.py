"""Arbitraje CEX <-> DEX: SOL/USDC en exchanges centralizados vs Jupiter (Solana).

Dos sentidos, con inventario prepuesto en el CEX y en la wallet:
  1) comprar SOL en el CEX (ask) y venderlo en el DEX (SOL -> USDC)
  2) comprar SOL en el DEX (USDC -> SOL) y venderlo en el CEX (bid)
No es atómico: si la transacción on-chain falla después de ejecutar el CEX,
queda una pata despareja (se modela con probabilidad ASSUMED).

Costos:
  * DEX: el fee de los pools va dentro de la cotización (VERIFIED por la ruta).
    La pata DEX se valúa con el MÍNIMO GARANTIZADO (otherAmountThreshold), no
    con el monto esperado: así el deslizamiento tolerado entra como costo.
  * Red: 5000 lamports + fee de prioridad (mediana observada, VERIFIED) x CU
    estimadas (ASSUMED).
  * CEX: comisión taker de nivel base (ASSUMED).
"""

from ..core import ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity, make_rng, walk
from ..fees import fee_cost, taker_fee
from .base import Module

SYMBOL = "SOL/USDC"
BASE_FEE_LAMPORTS = 5000
COMPUTE_UNITS = 300_000          # ASSUMED: CU típicas de un swap multi-ruta
TX_FAIL_PROB = 0.05              # ASSUMED: transacción on-chain fallida/expirada
MAX_SKEW_MS = 3000


def network_fee_usd(priority, sol_usd):
    micro = (priority or {}).get("median_micro_lamports_per_cu") or 0
    lamports = BASE_FEE_LAMPORTS + micro * COMPUTE_UNITS / 1e6
    return lamports / 1e9 * sol_usd


class CexDex(Module):
    name = "cex_dex"
    needs_crypto_books = True
    needs_dex = True
    tx_fail_prob = TX_FAIL_PROB      # falla on-chain (ASSUMED), se combina con la de la pata CEX

    def evaluate(self, snap, ctx):
        out = []
        dex = getattr(snap, "dex", None) or {}
        quotes = dex.get("quotes") or {}
        if not quotes:
            return out
        sol_usd = dex.get("sol_usd")
        net_fee = network_fee_usd(dex.get("priority_fee"), sol_usd)
        for v in sorted({k.split("|")[0] for k in snap.books}):
            b = snap.book(v, SYMBOL)
            if not b or not b.get("asks") or not b.get("bids"):
                continue
            fee_ref = snap.markets.get(snap.k(v, SYMBOL), {}).get("taker_ref")
            for k, q in quotes.items():
                direction, usd = k.split("|")
                out.append(self._evaluate(snap, v, b, direction, float(usd), q, fee_ref,
                                          net_fee, ctx))
        return out

    def _evaluate(self, snap, v, b, direction, usd, q, fee_ref, net_fee, ctx):
        o = Opportunity(
            strategy=self.name, key=f"{v}|{direction}|{usd:g}", tick=snap.tick, ts=snap.ts,
            venues=[v, "jupiter"], instruments=[SYMBOL, "SOL/USDC(dex)"],
            observed={"quote": q, "cex_ask": b["asks"][0], "cex_bid": b["bids"][0],
                      "cex_fetched": b.get("fetched_at")},
            assumptions=["inventario prepuesto en CEX y wallet", "no atómico entre CEX y DEX",
                         f"prob. de tx fallida {TX_FAIL_PROB}", f"{COMPUTE_UNITS} CU por swap"],
            stage="ESTIMATED", capital_usd=2 * usd)
        if direction == "SOL->USDC":            # comprar SOL en CEX, vender en DEX
            qty = q["in"] / 1e9
            got, cex_cost, fills = walk(b["asks"], qty)
            if got < qty - 1e-12:
                o.reason = "INSUFFICIENT_DEPTH"
                return o
            dex_min = q["min_out"] / 1e6
            o.gross_usd = q["out"] / 1e6 - cex_cost
            cex_notional = cex_cost
            o.observed["limit_cex"] = fills[-1][0]
            o.costs["deslizamiento_dex_tolerado"] = Cost((q["out"] - q["min_out"]) / 1e6, VERIFIED,
                                                         "out esperado - mínimo garantizado")
            o.observed["guaranteed_dex_leg"] = dex_min
        else:                                   # comprar SOL en DEX, vender en CEX
            sol_min, sol_exp = q["min_out"] / 1e9, q["out"] / 1e9
            got, proceeds_exp, fills = walk(b["bids"], sol_exp)
            if got < sol_exp - 1e-12:
                o.reason = "INSUFFICIENT_DEPTH"
                return o
            _, proceeds_min, _ = walk(b["bids"], sol_min)
            o.gross_usd = proceeds_exp - q["in"] / 1e6
            cex_notional = proceeds_exp
            o.observed["limit_cex"] = fills[-1][0]
            o.costs["deslizamiento_dex_tolerado"] = Cost(proceeds_exp - proceeds_min, VERIFIED,
                                                         "SOL esperado - mínimo garantizado")
        o.size = q["in"]
        o.costs["fee_cex"] = fee_cost(cex_notional, v, fee_ref)
        o.costs["fee_red_solana"] = Cost(net_fee, VERIFIED,
                                         "5000 lamports + prioridad mediana observada x CU (CU supuestas)")
        o.costs["tx_fallida_esperada"] = Cost(TX_FAIL_PROB * cex_notional * taker_fee(v, fee_ref)[0] * 2,
                                              ASSUMED, "prob. x deshacer la pata CEX")
        o.max_loss_usd = cex_notional * 0.01 + net_fee      # pata despareja ~1% + fee (ASSUMED)
        o.reason = "ESTIMATED_POSITIVE" if o.net_estimated_usd > 0 else "NET_NEGATIVE_AFTER_COSTS"
        return o

    def execute(self, o, snap, ctx):
        if o.reason != "ESTIMATED_POSITIVE":
            return
        dex = getattr(snap, "dex", None) or {}
        v, direction, usd = o.key.split("|")
        q1 = (dex.get("quotes_after") or {}).get(f"{direction}|{usd}")
        b1 = snap.book(v, SYMBOL, after=True)
        if not q1 or not b1:
            o.reason = "NO_QUOTE_AFTER_LATENCY"
            return
        rng = make_rng(ctx.seed, self.name, f"{snap.tick}:{o.key}")
        lim = o.observed["limit_cex"]
        fee = taker_fee(v, snap.markets.get(snap.k(v, SYMBOL), {}).get("taker_ref"))[0]
        net_fee = network_fee_usd(dex.get("priority_fee"), dex.get("sol_usd"))
        p_fail = 1 - (1 - ctx.exec_cfg.leg_fail_prob) * (1 - self.tx_fail_prob)
        failed = rng.random() < p_fail
        if direction == "SOL->USDC":
            qty = q1["in"] / 1e9
            lv = [(p, s) for p, s in ctx.registry.available(v, SYMBOL, "asks", b1["asks"]) if p <= lim]
            got, cost, fills = walk(lv, qty)
            ctx.registry.claim(v, SYMBOL, "asks", fills)
            if got < qty - 1e-12:
                net, status = -(cost * fee) if got else 0.0, "PARTIAL" if got else "DISAPPEARED"
            elif failed:   # el swap no salió: se deshace el SOL comprado en el CEX
                bid = b1["bids"][0][0] if b1.get("bids") else cost / qty
                net, status = -(cost - got * bid) - cost * fee * 2 - net_fee, "LEG_FAILED"
            else:          # se toma el MÍNIMO garantizado (conservador)
                net = q1["min_out"] / 1e6 - cost - cost * fee - net_fee
                status = "FILLED"
        else:
            sol = q1["min_out"] / 1e9
            lv = [(p, s) for p, s in ctx.registry.available(v, SYMBOL, "bids", b1["bids"]) if p >= lim]
            got, proceeds, fills = walk(lv, sol)
            ctx.registry.claim(v, SYMBOL, "bids", fills)
            if failed:     # el swap no salió: no hay SOL para vender, solo se pierde el fee
                net, status = -net_fee, "LEG_FAILED"
            elif got < sol - 1e-12:
                net, status = proceeds - q1["in"] / 1e6 * got / sol - proceeds * fee - net_fee, "PARTIAL"
            else:
                net = proceeds - q1["in"] / 1e6 - proceeds * fee - net_fee
                status = "FILLED"
        ctx.ledger.commit(o.capital_usd)
        ctx.ledger.release(o.capital_usd, net, {"key": o.key, "tick": snap.tick})
        o.stage = "SIMULATED"
        o.sim = {"status": status, "net_usd": net, "net_pct_capital": net / o.capital_usd,
                 "dex_quote_after": {k: q1[k] for k in ("out", "min_out", "slot")},
                 "latency_ms": snap.latency_ms}
        o.decision = ACCEPTED if status == "FILLED" else REJECTED
        o.reason = status
