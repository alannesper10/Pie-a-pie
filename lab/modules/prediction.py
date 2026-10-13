"""Arbitraje en mercados de predicción.

1) polymarket_buy_all_no: en un evento negRisk de Polymarket gana a lo sumo
   una opción, así que comprar NO en k opciones paga como mínimo k-1 (misma
   matemática que buy_all_no de Kalshi; no requiere exhaustividad). El capital
   queda bloqueado hasta la resolución: el neto es un MÍNIMO GARANTIZADO bajo
   ese supuesto, no una ganancia realizada.
2) cross_venue (Kalshi <-> Polymarket): SOLO pares verificados a mano en
   config/prediction_pairs.json. Las coincidencias automáticas se escriben
   como candidatas UNVERIFIED y nunca son ejecutables (reglas de resolución
   distintas = riesgo de perder ambas patas).
Kalshi interno (kalshi_current, buy_all_no, strike_inconsistency) ya corre en
Actions; el laboratorio solo LEE sus registros (data/) y no los recalcula.
"""

import difflib
import json
import math
import re
from pathlib import Path

from ..core import ACCEPTED, ASSUMED, REJECTED, VERIFIED, Cost, Opportunity, make_rng, walk
from ..fees import polymarket_fee
from .base import Module

PAIRS_FILE = Path("config") / "prediction_pairs.json"
NEAR_MISS_GROSS = -0.03
SUSPICIOUS_GROSS_RETURN = 0.10


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def leg_contribution(yes_bid, fee_schedule):
    """Aporte por acción NO al top of book: YES_bid - fee(NO a 1 - YES_bid)."""
    return yes_bid - polymarket_fee(1.0, 1.0 - yes_bid, fee_schedule).usd


def candidate_legs(event):
    """Patas válidas de un evento negRisk (opciones Yes/No con libro)."""
    legs = []
    for m in event.get("markets") or []:
        toks = m.get("tokens") or []
        outcomes = m.get("outcomes")
        if isinstance(outcomes, str):
            try:
                outcomes = json.loads(outcomes)
            except ValueError:
                outcomes = None
        if (not m.get("active") or m.get("closed") or not m.get("enableOrderBook")
                or len(toks) != 2 or (outcomes and outcomes != ["Yes", "No"])):
            continue
        bid = _f(m.get("bestBid"))
        if 0 < bid < 1 and leg_contribution(bid, m.get("feeSchedule")) > 0:
            legs.append(m)
    return legs


def select_tokens(events):
    """NO tokens a pedir al CLOB (solo eventos candidatos por el top of book)."""
    toks = []
    for e in events:
        legs = candidate_legs(e)
        if len(legs) >= 2 and sum(_f(m["bestBid"]) for m in legs) - 1 > NEAR_MISS_GROSS:
            toks.extend(m["tokens"][1] for m in legs)
    return toks


def bundle_walk(ladders, payout, fee_schedules, cap_usd, min_shares):
    """Barre libros de NO para paquetes (1 acción por pata) mientras el paquete
    marginal tenga neto > 0. -> (acciones, costo, fees, fills_por_pata)."""
    n = len(ladders)
    idx, rem = [0] * n, [l[0][1] for l in ladders]
    shares = 0.0
    while all(i < len(l) for i, l in zip(idx, ladders)):
        prices = [ladders[k][idx[k]][0] for k in range(n)]
        fee = sum(polymarket_fee(1.0, p, fs).usd for p, fs in zip(prices, fee_schedules))
        if payout - sum(prices) - fee <= 0:
            break
        q = min(rem)
        spent_so_far = sum(walk(l, shares)[1] for l in ladders)
        if spent_so_far + q * sum(prices) > cap_usd:
            q = max(0.0, (cap_usd - spent_so_far) / sum(prices))
            shares += q
            break
        shares += q
        for k in range(n):
            rem[k] -= q
            if rem[k] <= 1e-12:
                idx[k] += 1
                if idx[k] < len(ladders[k]):
                    rem[k] = ladders[k][idx[k]][1]
    shares = math.floor(shares * 100) / 100       # Polymarket: 2 decimales
    if shares < min_shares:
        return 0.0, 0.0, 0.0, []
    fills = [walk(l, shares)[2] for l in ladders]
    cost = sum(p * q for f in fills for p, q in f)
    fees = sum(polymarket_fee(q, p, fs).usd for f, fs in zip(fills, fee_schedules) for p, q in f)
    return shares, cost, fees, fills


class PolymarketBuyAllNo(Module):
    name = "polymarket_buy_all_no"
    needs_polymarket = True

    def evaluate(self, snap, ctx):
        out = []
        pm = snap.polymarket or {}
        books = pm.get("books", {})
        for e in pm.get("events", []):
            legs = candidate_legs(e)
            if len(legs) < 2:
                continue
            gross_top = sum(_f(m["bestBid"]) for m in legs) - 1
            if gross_top <= NEAR_MISS_GROSS:
                continue
            o = Opportunity(
                strategy=self.name, key=f"polymarket|{e.get('slug')}", tick=snap.tick, ts=snap.ts,
                venues=["polymarket"], instruments=[m["tokens"][1] for m in legs],
                observed={"gross_top_gamma": gross_top, "k": len(legs),
                          "yes_bids_gamma": [_f(m["bestBid"]) for m in legs]},
                assumptions=["negRisk: a lo sumo un ganador (garantía del contrato)",
                             "capital bloqueado hasta la resolución",
                             "fórmula de fee C*rate*p*(1-p) con rate de feeSchedule"])
            ladders, scheds, mins = [], [], []
            for m in legs:
                b = books.get(m["tokens"][1])
                if not b or not b.get("asks"):
                    o.reason = "NO_BOOK_FOR_LEG"
                    break
                ladders.append([tuple(x) for x in b["asks"]])
                scheds.append(m.get("feeSchedule"))
                mins.append(_f(m.get("orderMinSize")) or 5.0)
            else:
                self._estimate(o, ladders, scheds, max(mins), ctx)
            out.append(o)
        return out

    def _estimate(self, o, ladders, scheds, min_shares, ctx):
        k = len(ladders)
        payout = k - 1
        best = sum(l[0][0] for l in ladders)
        o.stage = "ESTIMATED"
        o.observed["best_no_asks"] = [l[0][0] for l in ladders]
        o.observed["best_bundle_cost"] = best
        if best > 0 and (payout - best) / best > SUSPICIOUS_GROSS_RETURN:
            o.reason = "SUSPICIOUS_EDGE_CHECK_RULES"
            o.gross_usd = payout - best
            return
        cap = ctx.ledger.capital * ctx.max_trade_fraction
        shares, cost, fees, fills = bundle_walk(ladders, payout, scheds, cap, min_shares)
        if shares <= 0:
            o.gross_usd = payout - best
            o.costs = {"fees": Cost(sum(polymarket_fee(1, l[0][0], s).usd
                                        for l, s in zip(ladders, scheds)), VERIFIED, "1 paquete ref.")}
            o.capital_usd = best
            o.reason = ("BUDGET_TOO_SMALL" if best * min_shares > cap else
                        "NO_EDGE_AFTER_FEES_OR_MIN_SIZE")
            return
        o.size, o.capital_usd = shares, cost + fees
        o.gross_usd = shares * payout - cost
        o.costs = {"fees_polymarket": Cost(fees, VERIFIED, "feeSchedule de la API"),
                   "profundidad": Cost(0.0, VERIFIED, "incluida: precios barridos")}
        o.observed["limits"] = [f[-1][0] for f in fills]
        o.observed["fee_schedules"] = scheds
        o.reason = "ESTIMATED_POSITIVE" if o.net_estimated_usd > 0 else "NET_NEGATIVE_AFTER_COSTS"

    def execute(self, o, snap, ctx):
        if o.reason != "ESTIMATED_POSITIVE":
            return
        if not ctx.ledger.can_commit(o.capital_usd):
            o.reason = "NO_CAPITAL"
            return
        after = (snap.polymarket or {}).get("books_after", {})
        rng = make_rng(ctx.seed, self.name, f"{snap.tick}:{o.key}")
        fills = []
        for tok, lim in zip(o.instruments, o.observed["limits"]):
            lv = [(p, q) for p, q in (after.get(tok) or {}).get("asks", []) if p <= lim + 1e-12]
            lv = ctx.registry.available("polymarket", tok, "asks", lv)
            got = 0.0 if rng.random() < ctx.exec_cfg.leg_fail_prob else walk(lv, o.size)[0]
            fills.append((tok, got, walk(lv, got)[2]))
        matched = min(g for _, g, _ in fills)
        for tok, _, f in fills:
            ctx.registry.claim("polymarket", tok, "asks", f)
        cost = fees = unwind = 0.0
        for (tok, got, f), sched in zip(fills, o.observed.get("fee_schedules") or [None] * len(fills)):
            c = sum(p * q for p, q in f)
            fees += sum(polymarket_fee(q, p, sched).usd for p, q in f)
            if not got:
                continue
            cost += c * matched / got
            if got > matched:          # acciones NO de más: se venden al bid real
                excess = got - matched
                bids = [(p, q) for p, q in (after.get(tok) or {}).get("bids", [])]
                sold, proceeds, _ = walk(bids, excess)
                sell_fee = sum(polymarket_fee(q, p, sched).usd for p, q in walk(bids, excess)[2])
                # lo que no se pudo vender se da por perdido (conservador)
                unwind += (c * excess / got) - proceeds + sell_fee + \
                    excess * (c / got) * ctx.exec_cfg.unwind_penalty
        k = len(fills)
        net_min = matched * (k - 1) - cost - fees - unwind
        status = "DISAPPEARED" if matched == 0 else (
            "PARTIAL" if matched < o.size - 1e-9 else "FILLED")
        o.stage = "SIMULATED"
        o.sim = {"status": status, "matched_shares": matched, "cost_usd": cost, "fees_usd": fees,
                 "unwind_usd": unwind, "net_usd": net_min, "realized": False,
                 "net_kind": "MINIMO_GARANTIZADO_A_RESOLUCION",
                 "net_pct_capital": net_min / (cost + fees) if cost else 0.0}
        if unwind:                               # pérdida de deshacer: realizada ya
            ctx.ledger.release(0.0, -unwind, {"key": o.key, "tick": snap.tick, "kind": "unwind"})
        if matched > 0:
            ctx.ledger.commit(cost + fees)       # bloqueado hasta la resolución
            o.decision = ACCEPTED
        else:
            o.decision = REJECTED
        o.reason = status


# ----------------------------------------------- Kalshi <-> Polymarket ---

def load_verified_pairs(path=PAIRS_FILE):
    """Solo pares con verified=True y quién/cuándo lo verificó."""
    if not Path(path).exists():
        return []
    pairs = json.loads(Path(path).read_text(encoding="utf-8")).get("pairs", [])
    return [p for p in pairs if p.get("verified") is True and p.get("verified_by")
            and p.get("verified_at")]


def kalshi_fee(shares, price):
    """Kalshi taker: ceil al centavo de 0.07 * C * P * (1-P) (ASSUMED como en kalshi_current)."""
    return math.ceil(round(0.07 * shares * price * (1 - price) * 100, 9)) / 100


def cross_venue_edge(k_yes_ask, k_no_ask, p_yes_ask, p_no_ask, p_sched, shares=1.0):
    """Mejor dirección: YES en un venue + NO en el otro paga 1 si resuelven igual."""
    out = []
    for name, kp, pp in (("YES_kalshi+NO_polymarket", k_yes_ask, p_no_ask),
                         ("NO_kalshi+YES_polymarket", k_no_ask, p_yes_ask)):
        if kp is None or pp is None:
            continue
        cost = (kp + pp) * shares
        fees = kalshi_fee(shares, kp) + polymarket_fee(shares, pp, p_sched).usd
        out.append((shares - cost - fees, name, cost, fees))
    return max(out) if out else None


class CrossVenuePrediction(Module):
    name = "prediction_cross_venue"
    nature = "unverifiable"  # reglas entre plataformas: solo pares verificados a mano

    def __init__(self, pairs=None):
        self.pairs = load_verified_pairs() if pairs is None else pairs

    def evaluate(self, snap, ctx):
        out = []
        for p in self.pairs:
            k = (snap.kalshi or {}).get(p["kalshi_ticker"])
            pm = (snap.polymarket or {}).get("books", {})
            yes_b, no_b = pm.get(p["polymarket_yes_token"]), pm.get(p["polymarket_no_token"])
            o = Opportunity(strategy=self.name, key=f"{p['kalshi_ticker']}~{p['polymarket_yes_token'][:10]}",
                            tick=snap.tick, ts=snap.ts, venues=["kalshi", "polymarket"],
                            instruments=[p["kalshi_ticker"], p["polymarket_yes_token"]],
                            observed={"pair": p},
                            assumptions=["reglas de resolución verificadas a mano como equivalentes"])
            if not k or not yes_b or not no_b:
                o.reason = "MISSING_BOOK"
                out.append(o)
                continue
            e = cross_venue_edge(k.get("yes_ask"), k.get("no_ask"),
                                 yes_b["asks"][0][0] if yes_b.get("asks") else None,
                                 no_b["asks"][0][0] if no_b.get("asks") else None,
                                 p.get("polymarket_fee_schedule"))
            o.stage = "ESTIMATED"
            if e is None:
                o.reason = "NO_QUOTES"
            else:
                net, direction, cost, fees = e
                o.gross_usd, o.capital_usd = 1 - cost, cost + fees
                o.costs = {"fees": Cost(fees, ASSUMED, "Kalshi 0.07 ceil + Polymarket feeSchedule")}
                o.observed["direction"] = direction
                o.reason = "ESTIMATED_POSITIVE_1_SHARE" if net > 0 else "NET_NEGATIVE_AFTER_COSTS"
            out.append(o)
        return out


def suggest_pairs(kalshi_events, polymarket_events, top=50, min_score=0.6):
    """Candidatas por similitud de títulos. SIEMPRE UNVERIFIED: hay que revisar
    reglas, fechas y fuentes de resolución a mano antes de marcar verified."""
    norm = lambda s: re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower())  # noqa: E731
    pm = [(norm(f"{e.get('title')} {m.get('groupItemTitle') or m.get('question')}"), e, m)
          for e in polymarket_events for m in e.get("markets") or []]
    out = []
    for ke in kalshi_events:
        for km in ke.get("markets") or []:
            kt = norm(f"{ke.get('title')} {km.get('yes_sub_title')}")
            for pt, e, m in pm:
                s = difflib.SequenceMatcher(None, kt, pt).ratio()
                if s >= min_score:
                    out.append({"score": round(s, 3), "kalshi_ticker": km.get("ticker"),
                                "kalshi_title": f"{ke.get('title')} / {km.get('yes_sub_title')}",
                                "polymarket_question": m.get("question"),
                                "polymarket_tokens": m.get("tokens"), "verified": False,
                                "status": "UNVERIFIED_CANDIDATE"})
    return sorted(out, key=lambda x: -x["score"])[:top]
