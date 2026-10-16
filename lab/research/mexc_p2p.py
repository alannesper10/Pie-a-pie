"""MEXC P2P ("Compra rápida" / "Venta rápida") en ARS: ¿el ciclo cierra con ganancia neta?

Solo investigación sobre capturas guardadas (lab/research/fx_capture.py).
La "Compra rápida" toma el anuncio vendedor más barato que acepta el monto;
la "Venta rápida", el anuncio comprador más caro. Rutas:

  M1  comprar USDT en P2P de MEXC -> vender USDT en P2P de MEXC (todo dentro de MEXC;
      los pesos llegan al banco del usuario: no hay retiro de ARS de un exchange)
  M2  comprar en P2P de MEXC -> retirar USDT (TRC20) a Binance -> vender en el libro de Binance

Filtros de contraparte (se informan por separado, nunca se mezclan):
  "any"        cualquier anuncio
  "plausible"  anunciante argentino, comerciante, ≥ 20 órdenes en 30 días, ≥ 98% de
               finalización, y precio a menos de 3% del medio del libro de Binance.
               Un precio muy alejado del mercado es en sí mismo una señal de riesgo
               (fraude, triangulación, condiciones ocultas): se excluye, no se "aprovecha".
"""

COSTS = {
    "mexc_p2p_fee": (0.0, "DESCONOCIDO: 0% (DataWallet) o 0,2% (TradersUnion); se simula 0 y 0,2%"),
    "usdt_trc20_withdraw": (1.0, "PUBLICADO por MEXC (artículo 2026): ~1 USDT, dinámico"),
    "binance_spot_taker": (0.001, "VERIFICADO: binance.com/en/fee/trading"),
}
MAX_DEV = 0.03


def _mid(snap):
    d = (snap.get("binance_usdtars") or {}).get("data") or {}
    if not d.get("bids") or not d.get("asks"):
        return None, []
    bids = [(float(p), float(q)) for p, q in d["bids"]]
    return (bids[0][0] + float(d["asks"][0][0])) / 2, bids


def plausible(ad, mid):
    try:
        rate = float(ad.get("complete_rate_30d") or 0)
    except ValueError:
        rate = 0.0
    return (ad.get("country") == "AR" and ad.get("merchant_type") in ("merchant", "prime")
            and (ad.get("done_30d") or 0) >= 20 and rate >= 0.98
            and mid is not None and abs(ad["price"] / mid - 1) < MAX_DEV)


def fits(ad, ars):
    return ad["min_ars"] <= ars <= min(ad["max_ars"], ad["qty"] * ad["price"])


def evaluate(snap, ars=150_000, flt="plausible", p2p_fee=0.0, withdraw_usdt=1.0, spot_fee=0.001):
    mid, bids = _mid(snap)
    ok = (lambda a: plausible(a, mid)) if flt == "plausible" else (lambda a: True)
    sells = [a for a in (snap.get("mexc_p2p_sell") or {}).get("data") or [] if ok(a) and fits(a, ars)]
    if not sells or mid is None:
        return None
    buy_ad = min(sells, key=lambda a: a["price"])
    usdt = ars / buy_ad["price"] * (1 - p2p_fee)
    out = {"ts": snap["ts"], "buy_price": buy_ad["price"], "buy_nick": buy_ad.get("nick"),
           "binance_mid": mid, "buy_dev_pct": (buy_ad["price"] / mid - 1) * 100}
    # M1: vender dentro de MEXC al mejor comprador que acepte el monto en pesos
    buyers = [a for a in (snap.get("mexc_p2p_buy") or {}).get("data") or []
              if ok(a) and a["min_ars"] <= usdt * a["price"] <= a["max_ars"] and a["qty"] >= usdt]
    if buyers:
        b = max(buyers, key=lambda a: a["price"])
        out["m1_sell_price"] = b["price"]
        out["m1_net_pct"] = (usdt * b["price"] * (1 - p2p_fee) / ars - 1) * 100
    # M2: retirar a Binance y vender en el libro (retiro de ARS de Binance: dato pendiente, aparte)
    left, got = usdt - withdraw_usdt, 0.0
    for p, q in bids:
        t = min(left, q)
        got += t * p
        left -= t
        if left <= 1e-9:
            break
    if left <= 1e-9:
        out["m2_net_pct_before_ars_withdraw"] = (got * (1 - spot_fee) / ars - 1) * 100
    return out


def summarize(rows, key):
    v = sorted(r[key] for r in rows if r and r.get(key) is not None)
    if not v:
        return {"n": 0}
    n = len(v)
    return {"n": n, "positive": sum(x > 0 for x in v), "min": v[0], "median": v[n // 2], "max": v[-1]}
