"""Diferenciales de dólar implícito entre emisoras argentinas (CCL y MEP).

Dos construcciones, siempre con PUNTAS (nunca cierres) y cantidades:

1) MEP entre emisoras, todo en BYMA (especie en pesos vs especie D en
   dólares MEP de la MISMA acción; no hace falta ratio):
     vender dólares caro en A:  comprar A en D (ask) y vender A en pesos (bid)
         -> recibo  bidARS_A / askD_A  pesos por dólar
     recomprar dólares barato en B:  comprar B en pesos (ask), vender B en D (bid)
         -> pago    askARS_B / bidD_B  pesos por dólar
     ganancia bruta = (bidARS_A/askD_A) / (askARS_B/bidD_B) - 1
   Cuatro operaciones en BYMA; posición final en acciones = 0.

2) CCL entre emisoras (acción local en pesos vs ADR en Nueva York, con ratio
   de conversión). Con inventario previo (local A y ADR B): vender local A,
   comprar ADR A, vender ADR B, comprar local B. Requiere cuenta en ambos
   mercados; la conversión ADR<->local (canje) NO se usa (demora días).

Clasificación por observación:
  NO_VERIFICABLE   puntas de momentos distintos (desfase > MAX_SKEW_S, p. ej.
                   BYMA con demora vs Nasdaq en tiempo real) o falta un dato
  SIN_EDGE         neto <= 0 con los costos
  POTENCIAL        neto > 0 con costos x1,5 y puntas simultáneas. NO es
                   arbitraje garantizado: la liquidación, las normas
                   cambiarias y la ejecución simultánea no están verificadas.

Costos: derecho de mercado BYMA 5 pb + IVA (VERIFICADO: comunicado de BYMA,
vigente desde 01/10/2025); comisión del broker ASSUMED (varía por broker);
en EE.UU. comisión ASSUMED y tasa SEC sobre ventas ASSUMED. Además se informa
el costo total de equilibrio: el máximo costo por operación que el
diferencial soporta.
"""

from datetime import datetime

from .stats import mean

BYMA_MARKET_FEE = 0.0005 * 1.21      # VERIFICADO: 5 pb (3 negociación + 2 post trade) + IVA 21%
BROKER_AR = 0.0025                   # ASSUMED: comisión típica de broker local (+IVA incluido)
BROKER_US = 0.0005                   # ASSUMED
SEC_FEE_SELL = 0.0000278             # ASSUMED (tasa SEC sobre ventas)
MAX_SKEW_S = 60                      # puntas con más de 60 s de diferencia: no simultáneas
SUSPICIOUS_GROSS = 0.10              # bruto > 10%: casi seguro un dato o ratio mal, nunca POTENCIAL
STRESS = 1.5

# Ratios ADR:acción local (públicos; se VERIFICAN por consistencia en ratio_check)
RATIOS = {"GGAL": ("GGAL", 10), "BMA": ("BMA", 10), "PAM": ("PAMP", 25), "YPF": ("YPFD", 1),
          "CEPU": ("CEPU", 10), "TGS": ("TGSU2", 5), "EDN": ("EDN", 20), "SUPV": ("SUPV", 5),
          "LOMA": ("LOMA", 5), "CRESY": ("CRES", 10), "IRS": ("IRSA", 10), "TEO": ("TECO2", 5)}
D_SPECIES = {"GGAL": "GGALD", "BMA": "BMA.D", "PAMP": "PAMPD", "YPFD": "YPFDD", "CEPU": "CEPUD",
             "TGSU2": "TGSUD", "EDN": "EDND", "SUPV": "SUPVD", "LOMA": "LOMAD", "CRES": "CRESD",
             "IRSA": "IRSAD", "TECO2": "TECOD"}


def cost_per_trade_ar(mult=1.0):
    return (BROKER_AR * mult) + BYMA_MARKET_FEE


def cost_per_trade_us(mult=1.0, sell=False):
    return BROKER_US * mult + (SEC_FEE_SELL if sell else 0.0)


def _q(row, side):
    """Puntas de data912: (precio, cantidad) o None."""
    if not row:
        return None
    p, q = row.get(f"px_{side}"), row.get(f"q_{side}")
    return (float(p), float(q)) if p and q and p > 0 and q > 0 else None


def mep_pairs(arg_stocks, mult=1.0):
    """Todas las combinaciones A (vender dólares) / B (comprar dólares) con las
    especies en pesos y D de data912. -> lista de dicts."""
    legs = {}
    for local, dsp in D_SPECIES.items():
        a, d = arg_stocks.get(local), arg_stocks.get(dsp)
        bid_ars, ask_ars, bid_d, ask_d = _q(a, "bid"), _q(a, "ask"), _q(d, "bid"), _q(d, "ask")
        legs[local] = {"sell_usd": (bid_ars[0] / ask_d[0], min(bid_ars[1], ask_d[1]) * ask_d[0])
                       if bid_ars and ask_d else None,
                       "buy_usd": (ask_ars[0] / bid_d[0], min(ask_ars[1], bid_d[1]) * bid_d[0])
                       if ask_ars and bid_d else None}
    out = []
    c = cost_per_trade_ar(mult)
    for a, la in legs.items():
        for b, lb in legs.items():
            if a == b or not la["sell_usd"] or not lb["buy_usd"]:
                continue
            gross = la["sell_usd"][0] / lb["buy_usd"][0] - 1
            usd = min(la["sell_usd"][1], lb["buy_usd"][1])        # USD ejecutables al top
            out.append({"kind": "MEP", "sell_usd_in": a, "buy_usd_in": b, "gross": gross,
                        "net": gross - 4 * c, "usd_capacity": usd,
                        "breakeven_cost_per_trade": gross / 4})
    return out


def ccl_pairs(local_quotes, adr_quotes, mult=1.0, allowed=None):
    """local_quotes: {ticker_local: (bid, bid_q, ask, ask_q)} en pesos;
    adr_quotes: {adr: (bid, bid_q, ask, ask_q)} en USD. allowed: ADRs con
    ratio verificado por consistencia (None = todos)."""
    legs = {}
    for adr, (loc, ratio) in RATIOS.items():
        if allowed is not None and adr not in allowed:
            continue
        lq, aq = local_quotes.get(loc), adr_quotes.get(adr)
        if not lq or not aq or not all(lq[i] for i in (0, 2)) or not all(aq[i] for i in (0, 2)):
            continue
        # vender dólares en A: comprar ADR (ask) y vender local (bid)
        sell = (lq[0] * ratio / aq[2], min(lq[1] / ratio, aq[3]) * aq[2])
        buy = (lq[2] * ratio / aq[0], min(lq[3] / ratio, aq[1]) * aq[0])
        legs[adr] = {"sell_usd": sell, "buy_usd": buy}
    out = []
    c_ar, c_us = cost_per_trade_ar(mult), cost_per_trade_us(mult)
    for a, la in legs.items():
        for b, lb in legs.items():
            if a == b:
                continue
            gross = la["sell_usd"][0] / lb["buy_usd"][0] - 1
            cost = 2 * c_ar + 2 * c_us + SEC_FEE_SELL
            out.append({"kind": "CCL", "sell_usd_in": a, "buy_usd_in": b, "gross": gross,
                        "net": gross - cost, "usd_capacity": min(la["sell_usd"][1], lb["buy_usd"][1]),
                        "breakeven_cost_per_trade": gross / 4})
    return out


def _ts(x):
    try:
        return datetime.fromisoformat(str(x).replace("Z", "+00:00")).timestamp()
    except (TypeError, ValueError):
        return None


def classify(pair, skew_s, net_stress):
    if pair["gross"] > SUSPICIOUS_GROSS:
        return "SOSPECHOSO_REVISAR_DATOS"
    if skew_s is None or skew_s > MAX_SKEW_S:
        return "NO_VERIFICABLE"
    if pair["net"] <= 0:
        return "SIN_EDGE"
    return "POTENCIAL" if net_stress > 0 else "SIN_EDGE"


def analyze_snapshot(snap):
    """-> lista de observaciones clasificadas (MEP con data912; CCL con
    data912 local+ADR y con BYMA(demorado)+Nasdaq)."""
    c = snap.ccl or {}
    obs = []
    stocks = c.get("arg_stocks") or {}
    if stocks:
        stress = {(p["sell_usd_in"], p["buy_usd_in"]): p for p in mep_pairs(stocks, STRESS)}
        for p in mep_pairs(stocks):
            ps = stress[(p["sell_usd_in"], p["buy_usd_in"])]
            # misma respuesta de la API para todas las patas: simultáneas entre sí,
            # pero la demora de data912 respecto del mercado NO está verificada
            obs.append({**p, "source": "data912", "skew_s": 0.0, "net_stress": ps["net"],
                        "verdict": classify(p, 0.0, ps["net"]), "tick": snap.tick, "ts": snap.ts})
    adrs = c.get("usa_adrs") or {}
    ok = {k for k, v in ratio_check(snap).items() if v["status"] == "CONSISTENTE"}
    if stocks and adrs:
        lq = {k: (v.get("px_bid"), v.get("q_bid"), v.get("px_ask"), v.get("q_ask")) for k, v in stocks.items()}
        aq = {k: (v.get("px_bid"), v.get("q_bid"), v.get("px_ask"), v.get("q_ask")) for k, v in adrs.items()}
        skew = abs((_ts(c.get("arg_stocks_fetched_at")) or 0) - (_ts(c.get("usa_adrs_fetched_at")) or 0))
        stress = {(p["sell_usd_in"], p["buy_usd_in"]): p for p in ccl_pairs(lq, aq, STRESS, ok)}
        for p in ccl_pairs(lq, aq, allowed=ok):
            ps = stress[(p["sell_usd_in"], p["buy_usd_in"])]
            obs.append({**p, "source": "data912", "skew_s": skew, "net_stress": ps["net"],
                        "verdict": classify(p, skew, ps["net"]), "tick": snap.tick, "ts": snap.ts})
    byma, nq = c.get("byma") or {}, c.get("nasdaq") or {}
    if byma and nq:
        lq = {}
        for k, v in byma.items():
            sym, settle = k.split("|")
            if settle == "2":                                   # 24 hs (plazo estándar)
                lq[sym] = (v.get("bidPrice"), v.get("quantityBid"), v.get("offerPrice"),
                           v.get("quantityOffer"))
        aq = {k: (v.get("bid"), v.get("bid_size"), v.get("ask"), v.get("ask_size")) for k, v in nq.items()}
        for p in ccl_pairs(lq, aq, allowed=ok or None):
            # BYMA gratuito tiene ~20 min de demora: puntas NO simultáneas
            obs.append({**p, "source": "byma_demorado+nasdaq", "skew_s": None, "net_stress": None,
                        "verdict": classify(p, None, None), "tick": snap.tick, "ts": snap.ts})
    return obs


def ratio_check(snap, tol=0.05):
    """Ratio verificado por consistencia: el CCL implícito (mid) de cada emisora
    debe quedar a menos de `tol` de la mediana de todas."""
    c = snap.ccl or {}
    stocks, adrs = c.get("arg_stocks") or {}, c.get("usa_adrs") or {}
    implied = {}
    for adr, (loc, ratio) in RATIOS.items():
        s, a = stocks.get(loc), adrs.get(adr)
        if s and a and s.get("px_bid") and s.get("px_ask") and a.get("px_bid") and a.get("px_ask"):
            implied[adr] = ((s["px_bid"] + s["px_ask"]) / 2 * ratio) / ((a["px_bid"] + a["px_ask"]) / 2)
    if not implied:
        return {}
    med = sorted(implied.values())[len(implied) // 2]
    return {k: {"implied_ccl": v, "dev_vs_median": v / med - 1,
                "status": "CONSISTENTE" if abs(v / med - 1) < tol else "NO_CONSISTENTE"}
            for k, v in implied.items()}


def episodes(obs, verdict="POTENCIAL"):
    """Rachas de ticks consecutivos con el mismo par en `verdict`: frecuencia y
    duración (en ticks) de cada oportunidad, sin contarla dos veces."""
    by = {}
    for o in obs:
        if o["verdict"] == verdict:
            by.setdefault((o["kind"], o["source"], o["sell_usd_in"], o["buy_usd_in"]), []).append(o)
    eps = []
    for key, lst in by.items():
        lst.sort(key=lambda o: o["tick"])
        cur = [lst[0]]
        for o in lst[1:]:
            if o["tick"] == cur[-1]["tick"] + 1:
                cur.append(o)
            else:
                eps.append((key, cur))
                cur = [o]
        eps.append((key, cur))
    return [{"kind": k[0], "source": k[1], "sell_usd_in": k[2], "buy_usd_in": k[3],
             "first_ts": c[0]["ts"], "last_ts": c[-1]["ts"], "ticks": len(c),
             "net_max": max(o["net"] for o in c), "net_mean": mean([o["net"] for o in c]),
             "usd_capacity_min": min(o["usd_capacity"] for o in c)} for k, c in eps]


def summarize(obs):
    from collections import Counter
    by_kind = {}
    for o in obs:
        k = f"{o['kind']}|{o['source']}"
        d = by_kind.setdefault(k, {"n": 0, "verdicts": Counter(), "gross": []})
        d["n"] += 1
        d["verdicts"][o["verdict"]] += 1
        d["gross"].append(o["gross"])
    out = {}
    for k, d in by_kind.items():
        g = sorted(d["gross"])
        out[k] = {"observations": d["n"], "verdicts": dict(d["verdicts"]),
                  "gross_max": g[-1], "gross_p95": g[int(0.95 * (len(g) - 1))],
                  "gross_median": g[len(g) // 2],
                  "breakeven_cost_per_trade_max": g[-1] / 4}
    return out
