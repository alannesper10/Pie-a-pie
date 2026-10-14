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


def p2p(trade_type, fiat="ARS", asset="USDT", pay_types=None):
    t0 = now()
    r = S.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", timeout=20,
               json={"asset": asset, "fiat": fiat, "tradeType": trade_type, "page": 1, "rows": 20,
                     "payTypes": pay_types or [], "publisherType": None})
    r.raise_for_status()
    ads = []
    for x in r.json().get("data") or []:
        a, u = x["adv"], x.get("advertiser") or {}
        ads.append({"price": float(a["price"]), "qty": float(a.get("tradableQuantity") or a.get("surplusAmount") or 0),
                    "min_ars": float(a.get("minSingleTransAmount") or 0),
                    "max_ars": float(a.get("maxSingleTransAmount") or 0),
                    "methods": [m.get("identifier") for m in a.get("tradeMethods") or []],
                    "pay_time_limit_min": a.get("payTimeLimit"),
                    "user_type": u.get("userType"), "orders_month": u.get("monthOrderCount"),
                    "finish_rate": u.get("monthFinishRate")})
    return {"fetched_at": t0, "data": ads}


SOURCES = {
    "data912_bonds": lambda: (lambda d: {"fetched_at": d["fetched_at"], "data": [
        x for x in d["data"] if x["symbol"].rstrip("DC") in BONDS or x["symbol"] in BONDS]})(
        get("https://data912.com/live/arg_bonds")),
    "binance_usdtars": lambda: get("https://api.binance.com/api/v3/depth", params={"symbol": "USDTARS", "limit": 100}),
    "bitso_usd_ars": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usd_ars"}),
    "bitso_usdt_ars": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usdt_ars"}),
    "bitso_usd_usdt": lambda: get("https://api.bitso.com/v3/order_book/", params={"book": "usd_usdt"}),
    "p2p_usdt_ars_buy": lambda: p2p("BUY"),     # anuncios donde el usuario COMPRA USDT
    "p2p_usdt_ars_sell": lambda: p2p("SELL"),   # anuncios donde el usuario VENDE USDT
    "p2p_usdt_usd_buy_ar": lambda: p2p("BUY", fiat="USD", pay_types=AR_METHODS),    # comprar USDT pagando USD local
    "p2p_usdt_usd_sell_ar": lambda: p2p("SELL", fiat="USD", pay_types=AR_METHODS),  # vender USDT cobrando USD local
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
