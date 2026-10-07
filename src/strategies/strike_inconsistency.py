"""strike_inconsistency: escaleras de strikes con precios no monótonos.

Dentro de UN grupo válido (mismo evento, misma variable, mismo sujeto):
  greater: P(v > X) >= P(v > Y) si X < Y   -> amplio B = X, angosto N = Y
  less:    P(v < Y) >= P(v < X) si X < Y   -> amplio B = Y, angosto N = X
Si YES_ask(B) < YES_bid(N): comprar YES en B + NO en N paga >= 1 siempre
(N implica B, así que nunca pierden las dos patas a la vez).

Protección contra el bug de agrupación (14.274 falsos candidatos al mezclar
jugadores/equipos dentro de un mismo evento):
  * clave = evento + strike_type + rules_primary normalizado (números -> #).
    Las reglas nombran sujeto y variable ("If Brayan Rocchio records # or more
    total bases"), así que dos sujetos nunca comparten clave.
  * además el ticker sin el strike final tiene que ser el mismo en todo el
    grupo, y cada raíz de ticker tiene que caer en un único grupo; si no,
    GROUPING_MISMATCH y se descarta.
  * strikes duplicados o faltantes: AMBIGUOUS_GROUP.
  * ganancia bruta > 10%: SUSPICIOUS_EDGE_CHECK_RULES (no ejecutable).

Solo lectura/paper: no envía órdenes.
"""

import re
from collections import Counter, defaultdict

from .kalshi_common import (
    asks_for, evaluate_bundle, fee_coefficient_for, leg_is_tradable,
    top_yes_ask, top_yes_bid,
)
from ..event_arbitrage import _num

STRATEGY = "strike_inconsistency"
NEAR_MISS_GROSS = -0.03
GREATER = {"greater", "greater_or_equal"}
LESS = {"less", "less_or_equal"}

_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
_TRAILING_STRIKE = re.compile(r"-?\d+(?:\.\d+)?$")


def rules_template(text):
    """Reglas con los números reemplazados por '#', minúsculas y espacios simples."""
    t = _NUMBER.sub("#", (text or "").lower())
    return re.sub(r"\s+", " ", t).strip()


def ticker_stem(ticker):
    """Ticker sin el número de strike final: 'EV-BALL20' -> 'EV-BALL'."""
    return _TRAILING_STRIKE.sub("", ticker or "")


def strike_of(m):
    st = m.get("strike_type")
    v = m.get("floor_strike") if st in GREATER else m.get("cap_strike")
    return None if v is None else float(v)


def build_groups(event):
    """Agrupa los mercados greater/less de un evento.

    Devuelve (grupos_válidos, Counter(motivos de descarte)).
    Cada grupo válido es una lista de mercados ordenada por strike.
    """
    reasons = Counter()
    raw = defaultdict(list)
    for m in event.get("markets") or []:
        st = m.get("strike_type")
        if st not in GREATER | LESS:
            continue
        if not m.get("rules_primary"):
            reasons["NO_RULES"] += 1
            continue
        key = (event.get("event_ticker"), st, rules_template(m["rules_primary"]))
        raw[key].append(m)

    # Cada raíz de ticker debe pertenecer a un único grupo de reglas.
    stem_groups = defaultdict(set)
    for key, ms in raw.items():
        for m in ms:
            stem_groups[(key[1], ticker_stem(m["ticker"]))].add(key)
    conflicted = {k for keys in stem_groups.values() if len(keys) > 1 for k in keys}

    groups = []
    for key, ms in raw.items():
        if len(ms) < 2:
            continue
        stems = {ticker_stem(m["ticker"]) for m in ms}
        if len(stems) > 1 or key in conflicted:
            reasons["GROUPING_MISMATCH"] += 1
            continue
        strikes = [strike_of(m) for m in ms]
        if any(s is None for s in strikes) or len(set(strikes)) != len(strikes):
            reasons["AMBIGUOUS_GROUP"] += 1
            continue
        groups.append(sorted(ms, key=strike_of))
    return groups, reasons


def pairs_in_group(group):
    """(amplio B, angosto N) para cada par de strikes del grupo."""
    st = group[0]["strike_type"]
    for i, lo in enumerate(group):
        for hi in group[i + 1:]:
            yield (lo, hi) if st in GREATER else (hi, lo)


def candidates_for_event(event, *, min_volume_24h=0.0):
    """Pares candidatos con el top of book anidado. -> (lista, Counter motivos)."""
    groups, reasons = build_groups(event)
    out = []
    for g in groups:
        for b, n in pairs_in_group(g):
            if not (leg_is_tradable(b) and leg_is_tradable(n)):
                reasons["LEG_NOT_TRADABLE"] += 1
                continue
            ask_b, bid_n = top_yes_ask(b), top_yes_bid(n)
            if not (0 < ask_b < 1 and 0 < bid_n < 1):
                reasons["NO_QUOTE"] += 1
                continue
            vol = _num(b.get("volume_24h_fp")) + _num(n.get("volume_24h_fp"))
            if vol < min_volume_24h:
                reasons["LOW_VOLUME"] += 1
                continue
            gross = bid_n - ask_b
            if gross <= NEAR_MISS_GROSS:
                reasons["PRELIM_GROSS_TOO_LOW"] += 1
                continue
            out.append({"event": event, "broad": b, "narrow": n, "gross_top": gross,
                        "coef": fee_coefficient_for(event)})
    return out, reasons


def evaluate(candidate, books, *, slippage=0.0, min_net_edge=0.0,
             budget_usd=float("inf")):
    b, n = candidate["broad"], candidate["narrow"]
    return evaluate_bundle(
        strategy=STRATEGY, event_ticker=candidate["event"].get("event_ticker", ""),
        key=f"{b['ticker']}|{n['ticker']}", tickers=[b["ticker"], n["ticker"]],
        sides=["yes", "no"],
        ladders=[asks_for(books[b["ticker"]], "yes"), asks_for(books[n["ticker"]], "no")],
        min_payout_per_bundle=1.0, fee_coefficient=candidate["coef"],
        slippage_per_contract=slippage, min_net_edge=min_net_edge,
        budget_usd=budget_usd,
        extra={"strike_type": b.get("strike_type"), "broad_strike": strike_of(b),
               "narrow_strike": strike_of(n),
               "gross_top_prefilter": round(candidate["gross_top"], 4)},
    )
