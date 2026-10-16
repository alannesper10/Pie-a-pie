"""C1 y C2 (BIBLIOTECA_HULL_ESTRATEGIAS_2026-10-16.md): opciones de BTC con trades reales de Deribit.

C2  strangle muy fuera del dinero COMPRADO (Hull, Business Snapshot 19.1: colas
    pesadas; Hull advierte que la oportunidad desapareció cuando el mercado la
    incorporó). Put delta ≈ −0,05 y call delta ≈ +0,05, 0,1 BTC, precio de ask
    (mediana de trades con dirección "buy"); capital = prima.
C1  volatilidad condicional (HIPÓTESIS PROPIA con herramientas de Hull, EN 22.2/22.6
    y BS 11.2): σ_EWMA(λ=0,94) frente a la IV ATM.
      σ_EWMA > 1,10·IV -> comprar straddle ATM (ask)
      σ_EWMA < 0,90·IV -> vender iron butterfly: straddle ATM al bid + alas delta ±0,10 al ask
      si no, sin operación. Capital = prima (straddle) o pérdida máxima (iron butterfly).
Ventana de entrada, vencimiento, costos y liquidación: iguales a P5
(lab/research/options_putspread.py). Lado faltante -> NO_VERIFICABLE.
"""

import math
from statistics import median

from .options_putspread import CAP, DELIVERY_FEE, FEE, Q, ncdf

LAMBDA = 0.94
HI, LO = 1.10, 0.90


def chain(trades, expiry_code):
    """{(strike, 'C'|'P'): [trades]} del vencimiento."""
    tag = f"BTC-{expiry_code}-"
    out = {}
    for t in trades:
        n = t["instrument_name"]
        if n.startswith(tag):
            _, _, k, cp = n.split("-")
            out.setdefault((int(k), cp), []).append(t)
    return out


def delta(S, K, T, iv, cp):
    if T <= 0 or iv <= 0:
        return None
    d1 = (math.log(S / K) + 0.5 * iv * iv * T) / (iv * math.sqrt(T))
    return ncdf(d1) if cp == "C" else ncdf(d1) - 1


def side_price(ts, direction):
    p = [t["price"] for t in ts if t["direction"] == direction]
    return median(p) if p else None


def fee(premium_btc, mult):
    return mult * min(FEE * Q, CAP * premium_btc * Q)


def dfee(payoff_usd, S_T, mult):
    return mult * min(DELIVERY_FEE * Q * S_T, CAP * payoff_usd) if payoff_usd > 0 else 0.0


def _setup(trades, expiry_code, entry, expiry):
    ch = chain(trades, expiry_code)
    if not ch:
        return None
    S = median(t["index_price"] for ts in ch.values() for t in ts)
    T = (expiry - entry).total_seconds() / (365 * 86400)
    d = {}
    for (k, cp), ts in ch.items():
        x = delta(S, k, T, median(t["iv"] for t in ts) / 100, cp)
        if x is not None:
            d[(k, cp)] = x
    return ch, S, T, d


def strangle(trades, expiry_code, entry, expiry, S_T, target=0.05, mult=1.0):
    st = _setup(trades, expiry_code, entry, expiry)
    if not st:
        return {"status": "NO_VERIFICABLE", "why": "sin trades del vencimiento"}
    ch, S, T, d = st
    puts = {k: v for (k, cp), v in d.items() if cp == "P"}
    calls = {k: v for (k, cp), v in d.items() if cp == "C"}
    if not puts or not calls:
        return {"status": "NO_VERIFICABLE", "why": "faltan puts o calls"}
    kp = min(puts, key=lambda k: abs(puts[k] + target))
    kc = min(calls, key=lambda k: abs(calls[k] - target))
    pp, pc = side_price(ch[(kp, "P")], "buy"), side_price(ch[(kc, "C")], "buy")
    if pp is None or pc is None:
        return {"status": "NO_VERIFICABLE", "why": "sin trade de compra en algún strike", "kp": kp, "kc": kc}
    cost = (pp + pc) * Q * S + (fee(pp, mult) + fee(pc, mult)) * S
    pay = (max(kp - S_T, 0) + max(S_T - kc, 0)) * Q
    pnl = pay - cost - dfee(pay, S_T, mult)
    return {"status": "OK", "S": S, "kp": kp, "kc": kc, "dp": puts[kp], "dc": calls[kc], "capital": cost,
            "payoff": pay, "pnl": pnl, "ret_pct": pnl / cost * 100, "days": T * 365}


def ewma_vol(closes, lam=LAMBDA):
    """σ anual EWMA (λ fijo, Hull EN 22.2) sobre retornos log diarios; sin mirar el futuro."""
    r = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    if len(r) < 31:
        return None
    var = sum(x * x for x in r[:30]) / 30
    for x in r[30:]:
        var = lam * var + (1 - lam) * x * x
    return math.sqrt(var * 365)


def conditional_vol(trades, expiry_code, entry, expiry, S_T, sigma_fc, mult=1.0):
    st = _setup(trades, expiry_code, entry, expiry)
    if not st:
        return {"status": "NO_VERIFICABLE", "why": "sin trades del vencimiento"}
    ch, S, T, d = st
    strikes = sorted({k for k, cp in ch if (k, "C") in ch and (k, "P") in ch})
    if not strikes:
        return {"status": "NO_VERIFICABLE", "why": "sin strike con call y put"}
    k0 = min(strikes, key=lambda k: abs(k - S))
    iv = median(t["iv"] for t in ch[(k0, "C")] + ch[(k0, "P")]) / 100
    base = {"S": S, "k0": k0, "iv": iv, "sigma_fc": sigma_fc, "days": T * 365}
    if sigma_fc > HI * iv:
        c, p = side_price(ch[(k0, "C")], "buy"), side_price(ch[(k0, "P")], "buy")
        if c is None or p is None:
            return {**base, "status": "NO_VERIFICABLE", "why": "sin ask ATM", "signal": "LONG_STRADDLE"}
        cost = (c + p) * Q * S + (fee(c, mult) + fee(p, mult)) * S
        pay = abs(S_T - k0) * Q
        pnl = pay - cost - dfee(pay, S_T, mult)
        return {**base, "status": "OK", "signal": "LONG_STRADDLE", "capital": cost, "pnl": pnl,
                "ret_pct": pnl / cost * 100}
    if sigma_fc < LO * iv:
        c, p = side_price(ch[(k0, "C")], "sell"), side_price(ch[(k0, "P")], "sell")
        calls = {k: v for (k, cp), v in d.items() if cp == "C" and k > k0}
        puts = {k: v for (k, cp), v in d.items() if cp == "P" and k < k0}
        if c is None or p is None or not calls or not puts:
            return {**base, "status": "NO_VERIFICABLE", "why": "sin bid ATM o sin alas", "signal": "SHORT_IRON_FLY"}
        kc = min(calls, key=lambda k: abs(calls[k] - 0.10))
        kp = min(puts, key=lambda k: abs(puts[k] + 0.10))
        wc, wp = side_price(ch[(kc, "C")], "buy"), side_price(ch[(kp, "P")], "buy")
        if wc is None or wp is None:
            return {**base, "status": "NO_VERIFICABLE", "why": "sin ask en las alas", "signal": "SHORT_IRON_FLY"}
        credit = (c + p - wc - wp) * Q * S - sum(fee(x, mult) for x in (c, p, wc, wp)) * S
        max_loss = max(kc - k0, k0 - kp) * Q - credit
        if max_loss <= 0:
            return {**base, "status": "NO_VERIFICABLE", "why": "crédito mayor que el ancho (dato anómalo)"}
        short_pay = abs(S_T - k0) * Q
        wings = (max(S_T - kc, 0) + max(kp - S_T, 0)) * Q
        pnl = credit - short_pay + wings - dfee(short_pay, S_T, mult) - dfee(wings, S_T, mult)
        return {**base, "status": "OK", "signal": "SHORT_IRON_FLY", "kc": kc, "kp": kp, "capital": max_loss,
                "pnl": pnl, "ret_pct": pnl / max_loss * 100}
    return {**base, "status": "SIN_SENAL"}
