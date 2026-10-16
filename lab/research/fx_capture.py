"""Captura de precios cambiarios ejecutables (solo lectura de APIs públicas).

Herramienta de INVESTIGACIÓN (no la usa el ejecutor ni el laboratorio).
Cada captura se agrega como una línea JSON a OUT (sin claves, sin órdenes).
Errores de una fuente quedan registrados en la captura; nunca se rellenan.

Uso: python -m lab.research.fx_capture OUT HASTA_HH:MM_ART INTERVALO_S [AAAA-MM-DDTHH:MM]
     (el último argumento opcional espera hasta esa hora argentina para empezar)
"""
import json
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

ART = timezone(timedelta(hours=-3))
BONDS = ["AL29", "AL30", "AL35", "AE38", "AL41", "GD29", "GD30", "GD35", "GD38", "GD41", "GD46"]
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (pie-a-pie research, read-only)"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def get(url, **kw):
    t0 = now()
    r = S.get(url, timeout=20, **kw)
    r.raise_for_status()
    return {"fetched_at": t0, "data": r.json()}


# medios de pago de cuentas argentinas (para USD: transferencia desde un banco o billetera local)
AR_METHODS = ["BankArgentina", "MercadoPagoNew", "UalaNew", "BancoBrubankNew", "NaranjaX",
              "SantanderArgentina", "BancoGalicia", "LemonCash", "BBVAArgentina"]


def p2p(trade_type, fiat="ARS", asset="USDT", pay_types=None, pages=1):
    """Anuncios P2P (endpoint público no documentado de Binance). Con pages > 1
    se leen varias páginas de 20; cada anuncio lleva su página y el userNo del
    anunciante para cruzarlo con su perfil."""
    t0 = now()
    ads = []
    for page in range(1, pages + 1):
        r = S.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", timeout=20,
                   json={"asset": asset, "fiat": fiat, "tradeType": trade_type, "page": page, "rows": 20,
                         "payTypes": pay_types or [], "publisherType": None})
        r.raise_for_status()
        rows = r.json().get("data") or []
        for x in rows:
            ads.append(_ad(x, page))
        if len(rows) < 20:
            break
    return {"fetched_at": t0, "data": ads}


def _ad(x, page=1):
    a, u = x["adv"], x.get("advertiser") or {}
    return {"price": float(a["price"]), "qty": float(a.get("tradableQuantity") or a.get("surplusAmount") or 0),
            "min_ars": float(a.get("minSingleTransAmount") or 0),
            "max_ars": float(a.get("maxSingleTransAmount") or 0),
            "methods": [m.get("identifier") for m in a.get("tradeMethods") or []],
            "pay_time_limit_min": a.get("payTimeLimit"),
            "user_type": u.get("userType"), "orders_month": u.get("monthOrderCount"),
            "finish_rate": u.get("monthFinishRate"), "positive_rate": u.get("positiveRate"),
            "user_no": u.get("userNo"), "nick": u.get("nickName"), "page": page,
            "classify": a.get("classify"), "extra_kyc": a.get("takerAdditionalKycRequired")}


MEXC_USDT_COIN_ID = "128f589271cb4951b03e71e6323eb7be"


def mexc_p2p(trade_type, pages=3):
    """Anuncios P2P de MEXC en ARS (endpoint público no documentado).
    trade_type="SELL": el anunciante VENDE USDT (el usuario compra; "Compra rápida").
    trade_type="BUY": el anunciante COMPRA USDT (el usuario vende; "Venta rápida")."""
    t0, ads = now(), []
    for page in range(1, pages + 1):
        r = S.get("https://p2p.mexc.com/api/market", timeout=20, params={
            "allowTrade": "false", "amount": "", "blockTrade": "false", "coinId": MEXC_USDT_COIN_ID,
            "countryCode": "", "currency": "ARS", "follow": "false", "haveTrade": "false", "page": page,
            "payMethod": "", "tradeType": trade_type})
        r.raise_for_status()
        rows = r.json().get("data") or []
        for a in rows:
            m, st = a.get("merchant") or {}, a.get("merchantStatistics") or {}
            ads.append({"id": a.get("id"), "price": a.get("price"), "qty": a.get("availableQuantity"),
                        "min_ars": a.get("minTradeLimit"), "max_ars": a.get("maxTradeLimit"),
                        "pay_methods": a.get("payMethod"), "country": a.get("countryCode"),
                        "kyc_level": a.get("kycLevel"), "min_register_days": a.get("minRegisterDate"),
                        "updated_ms": a.get("updateTime"), "terms": (a.get("tradeTerms") or "")[:300],
                        "member_id": m.get("memberId"), "nick": m.get("nickName"),
                        "merchant_type": m.get("merchantType"), "registry_ms": m.get("registry"),
                        "sells_total": st.get("totalSellCount"), "buys_total": st.get("totalBuyCount"),
                        "done_30d": st.get("doneLastMonthCount"),
                        "complete_rate_30d": st.get("lastMonthCompleteRate"),
                        "avg_handle_min": st.get("avgHandleTime"), "page": page})
        if len(rows) < 10:
            break
    return {"fetched_at": t0, "data": ads}


PROFILE_FIELDS = ("registerDays", "avgReleaseTimeOfLatest30day", "avgPayTimeOfLatest30day",
                  "finishRateLatest30day", "completedOrderNumOfLatest30day", "completedOrderNum", "counterpartyCount")
_seen_profiles = set()


def profiles(user_nos, max_new=15):
    """Perfil público de anunciantes NO vistos en este proceso (una vez por día
    de captura, como mucho `max_new` por captura para no saturar la API)."""
    t0, out = now(), {}
    new = [u for u in dict.fromkeys(user_nos) if u and u not in _seen_profiles]   # sin repetidos
    for u in new[:max_new]:
        r = S.get("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list",
                  params={"userNo": u}, timeout=20)
        r.raise_for_status()
        d = ((r.json().get("data") or {}).get("userDetailVo") or {})
        st = d.get("userStatsRet") or {}
        out[u] = {**{k: st.get(k) for k in PROFILE_FIELDS}, "kycStatus": d.get("kycStatus")}
        _seen_profiles.add(u)
    return {"fetched_at": t0, "data": out}


SOURCES = {
    "data912_bonds": lambda: (lambda d: {"fetched_at": d["fetched_at"], "data": [
        x for x in d["data"] if x["symbol"].rstrip("DC") in BONDS or x["symbol"] in BONDS]})(
        get("https://data912.com/live/arg_bonds")),
    "binance_usdtars": lambda: get("https://api.binance.com/api/v3/depth", params={"symbol": "USDTARS", "limit": 100}),
    "bitso_usd_ars": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usd_ars"}),
    "bitso_usdt_ars": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usdt_ars"}),
    "bitso_usd_usdt": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usd_usdt"}),
    "p2p_usdt_ars_buy": lambda: p2p("BUY", pages=3),     # anuncios donde el usuario COMPRA USDT (60)
    "p2p_usdt_ars_sell": lambda: p2p("SELL"),   # anuncios donde el usuario VENDE USDT
    "p2p_usdt_usd_buy_ar": lambda: p2p("BUY", fiat="USD", pay_types=AR_METHODS),    # comprar USDT pagando USD local
    "p2p_usdt_usd_sell_ar": lambda: p2p("SELL", fiat="USD", pay_types=AR_METHODS),  # vender USDT cobrando USD local
    "mexc_p2p_sell": lambda: mexc_p2p("SELL"),   # anunciantes que venden USDT (usuario compra)
    "mexc_p2p_buy": lambda: mexc_p2p("BUY"),     # anunciantes que compran USDT (usuario vende)
    "criptoya_bancos": lambda: get("https://criptoya.com/api/bancostodos"),
    "criptoya_usdt_ars": lambda: get("https://criptoya.com/api/usdt/ars/1000"),
    "criptoya_usdc_ars": lambda: get("https://criptoya.com/api/usdc/ars/1000"),
    "criptoya_usdt_usd": lambda: get("https://criptoya.com/api/usdt/usd/1000"),
    "criptoya_dolar": lambda: get("https://criptoya.com/api/dolar"),
    "dolarapi": lambda: get("https://dolarapi.com/v1/dolares"),
}


def capture(i):
    snap = {"i": i, "ts": now(), "errors": []}
    for k, fn in SOURCES.items():
        try:
            snap[k] = fn()
        except Exception as e:                       # se registra; nunca se rellena
            snap["errors"].append({"source": k, "error": f"{type(e).__name__}: {str(e)[:200]}"})
    try:
        buy = (snap.get("p2p_usdt_ars_buy") or {}).get("data") or []
        snap["p2p_profiles"] = profiles([a.get("user_no") for a in buy])
    except Exception as e:
        snap["errors"].append({"source": "p2p_profiles", "error": f"{type(e).__name__}: {str(e)[:200]}"})
    return snap


def main():
    out, until, interval = sys.argv[1], sys.argv[2], float(sys.argv[3])
    start = sys.argv[4] if len(sys.argv) > 4 else None          # AAAA-MM-DDTHH:MM (ART): esperar hasta entonces
    if start:
        t = datetime.strptime(start, "%Y-%m-%dT%H:%M").replace(tzinfo=ART)
        while datetime.now(ART) < t:                              # de a 60 s: tolera suspensión de la notebook
            time.sleep(min(60.0, (t - datetime.now(ART)).total_seconds() + 0.1))
    h, m = map(int, until.split(":"))
    end = datetime.now(ART).replace(hour=h, minute=m, second=0, microsecond=0)
    i = 0
    try:                                                          # reanudar la numeración si el archivo ya existe
        with open(out, encoding="utf-8") as f:
            i = sum(1 for _ in f)
    except FileNotFoundError:
        pass
    while datetime.now(ART) < end:
        t0 = time.monotonic()
        snap = capture(i)
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(snap, separators=(",", ":")) + "\n")
        print(f"{snap['ts']} captura {i} errores {len(snap['errors'])} {time.monotonic() - t0:.1f}s", flush=True)
        i += 1
        time.sleep(max(0.0, interval - (time.monotonic() - t0)))


if __name__ == "__main__":
    main()
