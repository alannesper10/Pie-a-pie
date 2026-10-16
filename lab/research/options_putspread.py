"""P5: venta mensual de put spread de BTC (Deribit) con precios históricos de operaciones reales.

No es una comparación de volatilidades: cada mes se reconstruye una OPERACIÓN con
los trades reales de Deribit (history.deribit.com) y se liquida contra el precio
de entrega oficial.

Regla FIJA (16/10/2026, antes de ver resultados):
  - vencimiento objetivo E: mensual (último viernes, 08:00 UTC)
  - entrada: el día del vencimiento mensual anterior, 08:00–12:00 UTC
  - con los trades de puts de E en esa ventana: delta Black-Scholes con la IV
    mediana de cada strike, el índice y el plazo; strike vendido = delta más
    cercano a −0,25; strike comprado = delta más cercano a −0,10 (más bajo)
  - precio de venta: mediana de los trades con dirección "sell" (el agresor vendió,
    precio de bid) del strike vendido; precio de compra: mediana de los "buy"
    (precio de ask) del strike comprado. Si falta alguno: el mes es NO VERIFICABLE
  - tamaño 0,1 BTC por pata; P&L en USD (prima × índice de entrada; pago con la
    entrega oficial btc_usd)
  - comisiones (SUPUESTO conservador, sin tabla oficial verificada): 0,04% del
    subyacente por pata con tope de 12,5% de la prima; entrega 0,015% por pata
    dentro del dinero, mismo tope
  - capital = pérdida máxima (ancho × 0,1 − prima neta): riesgo definido
  - muestra 2020–2023 / fuera 2024–2026; > 20% de meses no verificables -> prueba NO VERIFICABLE
"""

import calendar
import math
from datetime import datetime, timezone
from statistics import median

Q = 0.1
FEE = 0.0004
DELIVERY_FEE = 0.00015
CAP = 0.125


def last_friday(y, m):
    d = calendar.monthrange(y, m)[1]
    while datetime(y, m, d).weekday() != 4:
        d -= 1
    return datetime(y, m, d, 8, tzinfo=timezone.utc)


def code(dt):
    return f"{dt.day}{dt.strftime('%b').upper()}{dt.strftime('%y')}"


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def put_delta(S, K, T, iv):
    if T <= 0 or iv <= 0:
        return None
    d1 = (math.log(S / K) + 0.5 * iv * iv * T) / (iv * math.sqrt(T))
    return ncdf(d1) - 1


def fee_btc(premium_btc, rate=FEE):
    return min(rate * Q, CAP * premium_btc * Q) if premium_btc > 0 else rate * Q


def build_trade(trades, expiry, entry, delivery_usd, cost_mult=1.0):
    """trades: trades de opciones (dicts de Deribit) de la ventana de entrada.
    -> dict de la operación o {"status": "NO_VERIFICABLE", ...}."""
    tag = f"BTC-{code(expiry)}-"
    puts = {}
    for t in trades:
        n = t["instrument_name"]
        if n.startswith(tag) and n.endswith("-P"):
            puts.setdefault(int(n.split("-")[2]), []).append(t)
    if not puts:
        return {"status": "NO_VERIFICABLE", "why": "sin trades de puts del vencimiento"}
    S = median(t["index_price"] for ts in puts.values() for t in ts)
    T = (expiry - entry).total_seconds() / (365 * 86400)
    deltas = {}
    for k, ts in puts.items():
        d = put_delta(S, k, T, median(t["iv"] for t in ts) / 100)
        if d is not None:
            deltas[k] = d
    if len(deltas) < 2:
        return {"status": "NO_VERIFICABLE", "why": "menos de 2 strikes con IV"}
    k1 = min(deltas, key=lambda k: abs(deltas[k] + 0.25))
    lower = {k: v for k, v in deltas.items() if k < k1}
    if not lower:
        return {"status": "NO_VERIFICABLE", "why": "sin strike más bajo"}
    k2 = min(lower, key=lambda k: abs(lower[k] + 0.10))
    sells = [t["price"] for t in puts[k1] if t["direction"] == "sell"]
    buys = [t["price"] for t in puts[k2] if t["direction"] == "buy"]
    if not sells or not buys:
        return {"status": "NO_VERIFICABLE", "why": "sin trade ejecutable del lado necesario",
                "k1": k1, "k2": k2}
    p1, p2 = median(sells), median(buys)                       # BTC por BTC de subyacente
    fees = cost_mult * (fee_btc(p1) + fee_btc(p2))
    prem_usd = ((p1 - p2) * Q - fees) * S
    pay1 = max(k1 - delivery_usd, 0.0) * Q                     # pagamos (put vendido)
    pay2 = max(k2 - delivery_usd, 0.0) * Q                     # cobramos (put comprado)
    dfee = cost_mult * sum(min(DELIVERY_FEE * Q * delivery_usd, CAP * pay / Q * Q)
                           for pay in (pay1, pay2) if pay > 0)
    pnl = prem_usd - pay1 + pay2 - dfee
    max_loss = (k1 - k2) * Q - prem_usd
    if max_loss <= 0:
        return {"status": "NO_VERIFICABLE", "why": "prima mayor que el ancho (dato anómalo)"}
    return {"status": "OK", "S": S, "k1": k1, "k2": k2, "d1": deltas[k1], "d2": deltas[k2],
            "p1": p1, "p2": p2, "n_sell": len(sells), "n_buy": len(buys), "prem_usd": prem_usd,
            "delivery": delivery_usd, "pnl_usd": pnl, "max_loss_usd": max_loss,
            "ret_on_risk_pct": pnl / max_loss * 100, "days": T * 365}


# ---------------- datos públicos ----------------

def window_trades(s, t0_ms, t1_ms):
    out, start = [], t0_ms
    for _ in range(50):
        r = s.get("https://history.deribit.com/api/v2/public/get_last_trades_by_currency_and_time",
                  params={"currency": "BTC", "kind": "option", "start_timestamp": start,
                          "end_timestamp": t1_ms, "count": 1000, "sorting": "asc"}, timeout=60).json()
        res = r.get("result") or {}
        tr = res.get("trades") or []
        out += tr
        if not res.get("has_more") or not tr:
            break
        start = tr[-1]["timestamp"] + 1
    return out


def deliveries(s):
    out, offset = {}, 0
    while True:
        r = s.get("https://www.deribit.com/api/v2/public/get_delivery_prices",
                  params={"index_name": "btc_usd", "offset": offset, "count": 1000}, timeout=60).json()["result"]
        for x in r["data"]:
            out[x["date"]] = x["delivery_price"]
        offset += len(r["data"])
        if not r["data"] or offset >= r["records_total"]:
            break
    return out
