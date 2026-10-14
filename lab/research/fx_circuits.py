"""Análisis de circuitos cambiarios sobre las capturas de fx_capture.py.

Cada circuito arranca y termina en ARS (o en USD local cuando se indica) y se
evalúa con PUNTAS ejecutables y su profundidad. Las cotizaciones de CriptoYa y
dolarapi se tratan como INDICATIVAS (agregador / pizarra), nunca como precio
ejecutable verificado. Herramienta de INVESTIGACIÓN (no la usa el ejecutor).

Uso: python -m lab.research.fx_circuits capturas.jsonl salida.json
"""
import json
import statistics as st
import sys
from collections import defaultdict

BONDS = ["AL29", "AL30", "AL35", "AE38", "AL41", "GD29", "GD30", "GD35", "GD38", "GD41", "GD46"]

# --- costos (fuente y estado en COSTS_DOC) ---
BYMA_BOND_FEE = 0.0001 * 1.21      # SUPUESTO: derecho de mercado renta fija (no verificado) + IVA
BROKER_BOND = [0.0, 0.0025, 0.005]  # SUPUESTO: escenarios de comisión del broker por operación
BINANCE_TAKER = 0.001              # PUBLICADO (tarifa estándar spot 0,10%); no verificado para la cuenta
BITSO_TAKER = 0.006                # VERIFICADO: API pública de Bitso (available_books, flat_rate taker)
KRAKEN_TAKER = 0.002               # SUPUESTO: comisión en pares de stablecoins
KRAKEN_USDT_ASK = 0.99892          # OBSERVADO una vez (14/10 15:3x), libro público de Kraken
USDT_WITHDRAW = 5.0                # SUPUESTO: retiro USDT (red TRON) desde el exchange del exterior
WIRE_GALICIA = dict(pct=0.003, min_usd=125.0, usd_acct=0.001, intermediary=10.0, iva=0.21)  # VERIFICADO tarifario 29/08/2025


def wire_cost(usd):
    """Galicia, transferencia al exterior > USD 1.000 (tarifario 29/08/2025)."""
    c = WIRE_GALICIA
    galicia = max(usd * c["pct"], c["min_usd"]) + usd * c["usd_acct"]
    return galicia * (1 + c["iva"]) + c["intermediary"]


def walk(levels, amount, side_qty_is_base=True):
    """Precio promedio para `amount` unidades base recorriendo el libro; None si no alcanza."""
    left, cost = amount, 0.0
    for p, q in levels:
        take = min(left, q)
        cost += take * p
        left -= take
        if left <= 1e-12:
            return cost / amount
    return None


def bonds(snap):
    d = (snap.get("data912_bonds") or {}).get("data") or []
    out = {}
    for x in d:
        b, a, qb, qa = x.get("px_bid"), x.get("px_ask"), x.get("q_bid"), x.get("q_ask")
        if b and a and b > 0 and a > 0 and a >= b:
            out[x["symbol"]] = (b, qb or 0, a, qa or 0)
    return out


def fx_legs(bd, suffix):
    """Por bono: comprar USD (ARS ask / USD bid) y vender USD (ARS bid / USD ask), con capacidad en USD."""
    legs = {}
    for base in BONDS:
        loc, usd = bd.get(base), bd.get(base + suffix)
        if not loc or not usd:
            continue
        buy = loc[2] / usd[0]                       # ARS por USD al comprar dólares
        sell = loc[0] / usd[2]                      # ARS por USD al vender dólares
        cap_buy = min(loc[3], usd[1]) * usd[0] / 100   # VN * precio/100 = USD
        cap_sell = min(loc[1], usd[3]) * usd[2] / 100
        legs[base] = {"buy": buy, "sell": sell, "cap_buy": cap_buy, "cap_sell": cap_sell}
    return legs


def binance_book(snap):
    d = (snap.get("binance_usdtars") or {}).get("data") or {}
    return ([(float(p), float(q)) for p, q in d.get("bids", [])], [(float(p), float(q)) for p, q in d.get("asks", [])])


def bitso_book(snap, key):
    d = ((snap.get(key) or {}).get("data") or {}).get("payload") or {}
    return ([(float(x["price"]), float(x["amount"])) for x in d.get("bids", [])],
            [(float(x["price"]), float(x["amount"])) for x in d.get("asks", [])])


def analyze(snap, usd_sizes=(1000, 10000, 50000)):
    r = {"i": snap["i"], "ts": snap["ts"], "errors": [e["source"] for e in snap.get("errors", [])]}
    bd = bonds(snap)
    mep, ccl = fx_legs(bd, "D"), fx_legs(bd, "C")
    r["n_mep_bonds"], r["n_ccl_bonds"] = len(mep), len(ccl)
    costs4 = {b: 4 * (b + BYMA_BOND_FEE) for b in BROKER_BOND}

    # 1) MEP: ida y vuelta en el mismo bono y cruce entre bonos (4 operaciones en BYMA)
    if mep:
        best_buy = min(mep.items(), key=lambda kv: kv[1]["buy"])
        best_sell = max(mep.items(), key=lambda kv: kv[1]["sell"])
        r["mep_best_buy"], r["mep_best_sell"] = best_buy[1]["buy"], best_sell[1]["sell"]
        r["mep_cross_gross"] = best_sell[1]["sell"] / best_buy[1]["buy"] - 1
        r["mep_cross_pair"] = (best_buy[0], best_sell[0])
        r["mep_cross_cap_usd"] = min(best_buy[1]["cap_buy"], best_sell[1]["cap_sell"])
        r["mep_cross_net"] = {str(b): r["mep_cross_gross"] - c for b, c in costs4.items()}
        r["mep_roundtrip_al30"] = (mep["AL30"]["sell"] / mep["AL30"]["buy"] - 1) if "AL30" in mep else None
    if ccl:
        cb = min(ccl.items(), key=lambda kv: kv[1]["buy"])
        cs = max(ccl.items(), key=lambda kv: kv[1]["sell"])
        r["ccl_cross_gross"] = cs[1]["sell"] / cb[1]["buy"] - 1
        r["ccl_cross_pair"] = (cb[0], cs[0])
        r["ccl_cross_cap_usd"] = min(cb[1]["cap_buy"], cs[1]["cap_sell"])
        r["ccl_best_sell"] = cs[1]["sell"]
    # 2) canje (MEP -> cable -> ARS): BLOQUEADO por la DJ de 90 días; solo referencia
    if mep and ccl:
        r["canje_gross_ref"] = r["ccl_best_sell"] / r["mep_best_buy"] - 1

    # 3) cripto: libros ejecutables USDT/ARS
    bb, ba = binance_book(snap)
    xb, xa = bitso_book(snap, "bitso_usdt_ars")
    if bb and ba:
        r["binance_bid"], r["binance_ask"] = bb[0][0], ba[0][0]
        r["binance_roundtrip"] = bb[0][0] * (1 - BINANCE_TAKER) / (ba[0][0] * (1 + BINANCE_TAKER)) - 1
    if bb and xa:
        r["bitso_to_binance"] = bb[0][0] * (1 - BINANCE_TAKER) / (xa[0][0] * (1 + BITSO_TAKER)) - 1
    if xb and ba:
        r["binance_to_bitso"] = xb[0][0] * (1 - BITSO_TAKER) / (ba[0][0] * (1 + BINANCE_TAKER)) - 1
    # P2P: precio de anuncios (comisión Binance P2P al usuario no verificada; contraparte y límites)
    pbuy = (snap.get("p2p_usdt_ars_buy") or {}).get("data") or []     # el usuario compra USDT
    psell = (snap.get("p2p_usdt_ars_sell") or {}).get("data") or []   # el usuario vende USDT
    if pbuy:
        r["p2p_buy_best"] = min(a["price"] for a in pbuy)
    if psell:
        r["p2p_sell_best"] = max(a["price"] for a in psell)
    if pbuy and bb:
        r["p2p_to_binance"] = bb[0][0] * (1 - BINANCE_TAKER) / r["p2p_buy_best"] - 1
        ad = min(pbuy, key=lambda a: a["price"])
        r["p2p_best_ad"] = {k: ad.get(k) for k in ("price", "qty", "min_ars", "max_ars", "methods", "user_type",
                                                     "orders_month", "finish_rate")}
        # anuncios que dejan ganancia contra el bid de Binance, con su capacidad máxima en USDT
        good = [a for a in pbuy if bb[0][0] * (1 - BINANCE_TAKER) / a["price"] - 1 > 0]
        r["p2p_to_binance_ads"] = len(good)
        r["p2p_to_binance_cap_usdt"] = sum(min(a["qty"], a["max_ars"] / a["price"]) for a in good)
        r["p2p_to_binance_merchant_ads"] = sum(1 for a in good if a.get("user_type") == "merchant")
    if psell and ba:
        r["binance_to_p2p"] = r["p2p_sell_best"] / (ba[0][0] * (1 + BINANCE_TAKER)) - 1
    if pbuy and psell:
        r["p2p_roundtrip"] = r["p2p_sell_best"] / r["p2p_buy_best"] - 1
    # CriptoYa (INDICATIVO): mejor compra / mejor venta entre exchanges con comisiones según CriptoYa
    cy = (snap.get("criptoya_usdt_ars") or {}).get("data") or {}
    ref = (bb[0][0] + ba[0][0]) / 2 if bb and ba else None
    ok = lambda x: x and (ref is None or abs(x / ref - 1) < 0.03)   # > 3% del mid de Binance: sospechoso
    asks = {k: v["totalAsk"] for k, v in cy.items() if isinstance(v, dict) and ok(v.get("totalAsk"))}
    bids = {k: v["totalBid"] for k, v in cy.items() if isinstance(v, dict) and ok(v.get("totalBid"))}
    r["cy_suspicious"] = sorted(k for k, v in cy.items() if isinstance(v, dict) and
                                ((v.get("totalBid") and not ok(v["totalBid"])) or (v.get("totalAsk") and not ok(v["totalAsk"]))))
    if asks and bids:
        ka, kb = min(asks, key=asks.get), max(bids, key=bids.get)
        r["cy_cross_gross"] = bids[kb] / asks[ka] - 1
        r["cy_cross_pair"] = (ka, kb)

    # 4) MEP <-> cripto en el país (USD local <-> USDT en plataformas locales; INDICATIVO CriptoYa usdt/usd)
    cu = (snap.get("criptoya_usdt_usd") or {}).get("data") or {}
    uask = {k: v["totalAsk"] for k, v in cu.items() if isinstance(v, dict) and v.get("totalAsk") and v.get("time", 0) > 0}
    ubid = {k: v["totalBid"] for k, v in cu.items() if isinstance(v, dict) and v.get("totalBid")}
    if mep and bb and uask:
        r["usdt_usd_ask_by_venue"] = uask
        # ARS -> MEP (comprar USD) -> USDT con USD local -> vender USDT en Binance
        r["mep_to_crypto_by_venue"] = {k: bb[0][0] * (1 - BINANCE_TAKER) / (r["mep_best_buy"] * a) - 1
                                       for k, a in uask.items()}
    if mep and ba and ubid:
        # ARS -> USDT (Binance) -> vender USDT por USD local -> vender MEP
        r["crypto_to_mep_by_venue"] = {k: r["mep_best_sell"] * b / (ba[0][0] * (1 + BINANCE_TAKER)) - 1
                                       for k, b in ubid.items()}

    # 5) Oficial (pizarra BNA vía dolarapi, INDICATIVO) -> USDT local o vía exterior
    da = (snap.get("dolarapi") or {}).get("data") or []
    of = next((x for x in da if x.get("casa") == "oficial"), None)
    if of:
        r["oficial_venta"] = of["venta"]
    # 6) Vía exterior: (MEP u oficial) -> transferencia a cuenta propia -> Kraken USDT -> Binance ARS
    if bb:
        for origin, px in (("mep", r.get("mep_best_buy")), ("oficial", r.get("oficial_venta"))):
            if not px:
                continue
            for usd in usd_sizes:
                usd_out = usd - wire_cost(usd)
                usdt = usd_out / KRAKEN_USDT_ASK * (1 - KRAKEN_TAKER) - USDT_WITHDRAW
                avg = walk(bb, usdt)
                if avg is None:
                    r[f"ext_{origin}_{usd}"] = None          # el libro no alcanza: no ejecutable
                    continue
                ars_back = usdt * avg * (1 - BINANCE_TAKER)
                r[f"ext_{origin}_{usd}"] = ars_back / (usd * px) - 1
        r["binance_bid_depth_usdt_1pct"] = sum(q for p, q in bb if p >= bb[0][0] * 0.99)
    return r


def summarize(rows):
    def dist(vals):
        vals = sorted(v for v in vals if v is not None)
        if not vals:
            return None
        n = len(vals)
        return {"n": n, "min": vals[0], "p25": vals[n // 4], "median": vals[n // 2],
                "p75": vals[3 * n // 4], "max": vals[-1], "positive": sum(v > 0 for v in vals)}
    keys = ["mep_roundtrip_al30", "mep_cross_gross", "ccl_cross_gross", "canje_gross_ref", "binance_roundtrip",
            "bitso_to_binance", "binance_to_bitso", "p2p_to_binance", "binance_to_p2p", "p2p_roundtrip",
            "cy_cross_gross", "mep_cross_cap_usd", "p2p_to_binance_ads", "p2p_to_binance_cap_usdt",
            "p2p_to_binance_merchant_ads", "binance_bid_depth_usdt_1pct"]
    keys += [k for k in rows[0] if k.startswith("ext_")] if rows else []
    out = {k: dist([r.get(k) for r in rows]) for k in keys}
    for b in BROKER_BOND:
        out[f"mep_cross_net_broker_{b}"] = dist([(r.get("mep_cross_net") or {}).get(str(b)) for r in rows])
    venues = defaultdict(list)
    for r in rows:
        for k, v in (r.get("mep_to_crypto_by_venue") or {}).items():
            venues[k].append(v)
    out["mep_to_crypto_by_venue"] = {k: dist(v) for k, v in venues.items()}
    venues = defaultdict(list)
    for r in rows:
        for k, v in (r.get("crypto_to_mep_by_venue") or {}).items():
            venues[k].append(v)
    out["crypto_to_mep_by_venue"] = {k: dist(v) for k, v in venues.items()}
    pairs = defaultdict(int)
    for r in rows:
        if r.get("mep_cross_pair"):
            pairs["/".join(r["mep_cross_pair"])] += 1
    out["mep_cross_pairs"] = dict(pairs)
    pairs = defaultdict(int)
    for r in rows:
        if r.get("cy_cross_pair"):
            pairs["->".join(r["cy_cross_pair"])] += 1
    out["cy_cross_pairs"] = dict(pairs)
    errs = defaultdict(int)
    for r in rows:
        for e in r["errors"]:
            errs[e] += 1
    out["errors"] = dict(errs)
    sus = defaultdict(int)
    for r in rows:
        for k in r.get("cy_suspicious") or []:
            sus[k] += 1
    out["cy_suspicious"] = dict(sus)
    out["captures"] = len(rows)
    out["first_ts"], out["last_ts"] = rows[0]["ts"], rows[-1]["ts"]
    out["wire_cost_usd"] = {u: wire_cost(u) for u in (1000, 10000, 50000)}
    return out


if __name__ == "__main__":
    rows = [analyze(json.loads(l)) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    s = summarize(rows)
    json.dump({"summary": s, "rows": rows}, open(sys.argv[2], "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps(s, indent=1, default=str)[:6000])
