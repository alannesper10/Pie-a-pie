"""Futuros con vencimiento: cash-and-carry y estructura temporal.

cash_and_carry (candidato a arbitraje): comprar spot (ask) y vender el futuro
(bid) del MISMO exchange, y mantener hasta el vencimiento. Al vencer, el futuro
liquida contra el índice del exchange (cláusula contractual), así que el
resultado por unidad queda fijado en (F0 - S0) menos costos, sin depender de
adivinar el precio. Riesgos residuales que se listan siempre:
  * índice de liquidación vs precio al que se vende el spot (ASSUMED),
  * margen: a 1x un short se liquida si el precio ~se duplica antes del
    vencimiento sin reponer margen (hay que mover el spot como garantía),
  * contraparte del exchange.
El capital queda bloqueado hasta el vencimiento (lock_hours). NO se anualiza.

calendar_spread (estadístico): diferencias entre vencimientos. Mantener una
posición near/far depende de cómo se mueva la base futura: se registra como
observación; sin un modelo validado no es arbitraje.
"""

from ..core import ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity, make_rng, walk
from ..fees import SETTLEMENT_FEE, fee_cost, futures_taker_fee, taker_fee
from .base import Module

ALLOCATION = 0.9             # 10% de reserva para margen
LEVERAGE = 1.0
INDEX_DEVIATION = 0.0005     # ASSUMED: índice de liquidación vs nuestra venta spot
MAX_LOSS_FRACTION = 0.005    # ASSUMED: si la convergencia al índice falla parcialmente
LIMIT_TOLERANCE = 0.0005     # ASSUMED: tolerancia del límite (mantener hasta vencimiento,
                             # no es un disparo de latencia); el neto usa los precios de T1
HOUR_MS = 3_600_000


def _ms(iso):
    from datetime import datetime
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


class TermStructure(Module):
    name = "cash_and_carry"
    needs_futures = True

    def evaluate(self, snap, ctx):
        fut = getattr(snap, "futures", None) or {}
        books, meta = fut.get("books") or {}, fut.get("meta") or {}
        out = []
        now = _ms(snap.ts)
        for k, m in sorted(meta.items()):
            fb, sb = books.get(k), books.get(snap.k(m["venue"], m["spot"]))
            if not fb or not sb or not fb.get("bids") or not sb.get("asks"):
                out.append(self._obs(snap, m, "NO_BOOK_FOR_LEG"))
                continue
            out.append(self._evaluate(snap, ctx, m, sb, fb, now))
        return out

    def _obs(self, snap, m, reason):
        o = Opportunity(strategy=self.name, key=f"{m['venue']}|{m['symbol']}", tick=snap.tick,
                        ts=snap.ts, venues=[m["venue"]], instruments=[m["spot"], m["symbol"]],
                        observed={"expiry": m.get("expiry_iso")}, reason=reason)
        return o

    def _evaluate(self, snap, ctx, m, sb, fb, now):
        v = m["venue"]
        o = self._obs(snap, m, "")
        hours = (m["expiry"] - now) / HOUR_MS
        o.lock_hours, o.valid_until = hours, m.get("expiry_iso")
        s_ask, f_bid = sb["asks"][0][0], fb["bids"][0][0]
        o.observed.update({"spot_ask": sb["asks"][0], "fut_bid": fb["bids"][0],
                           "basis_pct": (f_bid - s_ask) / s_ask, "hours_to_expiry": hours,
                           "fetched": [sb.get("fetched_at"), fb.get("fetched_at")]})
        o.assumptions = ["mantener hasta el vencimiento", "1x de apalancamiento",
                         "el futuro converge al índice de liquidación",
                         f"desvío índice vs venta spot {INDEX_DEVIATION:.2%}"]
        notional = ctx.ledger.capital * ALLOCATION / (1 + 1 / LEVERAGE)
        qty = notional / s_ask
        mins = [x for x in (m.get("min_amount"), m.get("spot_min_amount")) if x]
        if any(qty < x for x in mins) or (m.get("min_cost") and notional < m["min_cost"]):
            need = max([x * s_ask for x in mins] + [m.get("min_cost") or 0])
            o.reason = "INFEASIBLE_MIN_SIZE"
            o.observed["min_capital_usd"] = need * (1 + 1 / LEVERAGE) / ALLOCATION
            q = max(mins) if mins else qty            # referencia al tamaño mínimo
        else:
            q = qty
        got_s, cost_s, fill_s = walk(sb["asks"], q)
        got_f, proc_f, fill_f = walk(fb["bids"], q)
        if got_s < q - 1e-12 or got_f < q - 1e-12:
            o.reason = o.reason or "INSUFFICIENT_DEPTH"
            return o
        o.stage, o.size = "ESTIMATED", q
        o.capital_usd = cost_s + proc_f / LEVERAGE
        o.gross_usd = proc_f - cost_s                  # base fijada al entrar
        fs, _ = taker_fee(v, m.get("spot_taker_ref"))
        ff, _ = futures_taker_fee(v, m.get("taker_ref"))
        o.costs = {
            "fee_spot_entrada": fee_cost(cost_s, v, m.get("spot_taker_ref")),
            "fee_futuro_entrada": Cost(proc_f * ff, ASSUMED, "taker futuros, nivel base"),
            "fee_spot_salida": Cost(cost_s * fs, ASSUMED, "venta spot al vencimiento (sobre S0)"),
            "fee_liquidacion_futuro": Cost(proc_f * SETTLEMENT_FEE, ASSUMED, "liquidación/entrega"),
            "desvio_indice": Cost(cost_s * INDEX_DEVIATION, ASSUMED, "índice vs venta spot"),
            "profundidad": Cost(0.0, VERIFIED, "incluida: precios promedio barridos"),
        }
        o.max_loss_usd = o.capital_usd * MAX_LOSS_FRACTION + sum(c.usd for c in o.costs.values())
        o.observed.update({"limit_spot": fill_s[-1][0], "limit_fut": fill_f[-1][0],
                           "period_return_pct": o.net_estimated_usd / o.capital_usd,
                           "return_per_day_locked_pct": (o.net_estimated_usd / o.capital_usd)
                           / max(hours / 24, 1e-9)})
        if not o.reason:
            o.reason = "ESTIMATED_POSITIVE" if o.net_estimated_usd > 0 else "NET_NEGATIVE_AFTER_COSTS"
        return o

    def execute(self, o, snap, ctx):
        if o.reason != "ESTIMATED_POSITIVE":
            return
        if not ctx.ledger.can_commit(o.capital_usd):
            o.reason = "NO_CAPITAL"
            return
        after = (getattr(snap, "futures", None) or {}).get("books_after") or {}
        v, sym = o.venues[0], o.instruments[1]
        sb, fb = after.get(snap.k(v, o.instruments[0])), after.get(snap.k(v, sym))
        if not sb or not fb:
            o.reason = "NO_BOOK_AFTER_LATENCY"
            return
        rng = make_rng(ctx.seed, self.name, f"{snap.tick}:{o.key}")
        lim_s = o.observed["limit_spot"] * (1 + LIMIT_TOLERANCE)
        lim_f = o.observed["limit_fut"] * (1 - LIMIT_TOLERANCE)
        lv_s = [(p, q) for p, q in ctx.registry.available(v, o.instruments[0], "asks", sb["asks"])
                if p <= lim_s]
        lv_f = [(p, q) for p, q in ctx.registry.available(v, sym, "bids", fb["bids"])
                if p >= lim_f]
        gs, cs, fs_ = walk(lv_s, o.size)
        failed = rng.random() < ctx.exec_cfg.leg_fail_prob
        gf, pf, ff_ = (0.0, 0.0, []) if failed else walk(lv_f, o.size)
        ctx.registry.claim(v, o.instruments[0], "asks", fs_)
        ctx.registry.claim(v, sym, "bids", ff_)
        matched = min(gs, gf)
        unwind = 0.0
        if gs > matched:   # spot comprado sin cobertura: se vende al bid con penalidad
            bid = sb["bids"][0][0] if sb.get("bids") else cs / gs
            unwind = (gs - matched) * (cs / gs - bid) + (gs - matched) * bid * (
                taker_fee(v)[0] + ctx.exec_cfg.unwind_penalty)
        costs_scale = matched / o.size if o.size else 0
        base_locked = matched * ((pf / gf if gf else 0) - (cs / gs if gs else 0))
        net = base_locked - sum(c.usd for c in o.costs.values()) * costs_scale - unwind
        status = ("DISAPPEARED" if matched == 0 and not failed else "LEG_FAILED" if failed
                  else "PARTIAL" if matched < o.size - 1e-12 else "FILLED")
        if matched > 0:
            ctx.ledger.commit(o.capital_usd * costs_scale)   # bloqueado hasta el vencimiento
        if unwind:
            ctx.ledger.release(0.0, -unwind, {"key": o.key, "kind": "unwind"})
        o.stage = "SIMULATED"
        o.sim = {"status": status, "matched": matched, "net_usd": net, "unwind_usd": unwind,
                 "realized": False, "net_kind": "BASE_FIJADA_A_VENCIMIENTO",
                 "net_pct_capital": net / o.capital_usd if o.capital_usd else 0.0,
                 "lock_hours": o.lock_hours}
        o.decision = ACCEPTED if status == "FILLED" else REJECTED
        o.reason = status


class CalendarSpread(Module):
    """Observaciones de la curva (near vs far). No es arbitraje sin modelo."""
    name = "calendar_spread"
    nature = "statistical"
    needs_futures = True

    def evaluate(self, snap, ctx):
        fut = getattr(snap, "futures", None) or {}
        books, meta = fut.get("books") or {}, fut.get("meta") or {}
        by = {}
        for k, m in meta.items():
            by.setdefault((m["venue"], m["asset"]), []).append((m["expiry"], k, m))
        out = []
        for (v, asset), lst in sorted(by.items()):
            lst.sort()
            for (e1, k1, m1), (e2, k2, m2) in zip(lst, lst[1:]):
                b1, b2 = books.get(k1), books.get(k2)
                if not b1 or not b2 or not b1.get("asks") or not b2.get("bids"):
                    continue
                mid1 = (b1["bids"][0][0] + b1["asks"][0][0]) / 2
                mid2 = (b2["bids"][0][0] + b2["asks"][0][0]) / 2
                days = (e2 - e1) / 86_400_000
                out.append(Opportunity(
                    strategy=self.name, key=f"{v}|{m1['symbol']}~{m2['symbol']}", tick=snap.tick,
                    ts=snap.ts, venues=[v], instruments=[m1["symbol"], m2["symbol"]],
                    observed={"near_mid": mid1, "far_mid": mid2, "days_between": days,
                              "forward_basis_pct": (mid2 - mid1) / mid1},
                    reason="OBSERVATION_NO_MODEL",
                    assumptions=["observación de la curva; requiere modelo validado"]))
        return out
