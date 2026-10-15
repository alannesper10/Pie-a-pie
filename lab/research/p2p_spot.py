"""Simulación del circuito P2P (compra de USDT) -> libro de Binance (venta) -> retiro de ARS.

Solo investigación: no consulta APIs ni opera. Recorre capturas guardadas
(lab/research/fx_capture.py) en orden y ejecuta ciclos SECUENCIALES, sin
solaparse: no empieza un ciclo hasta que el capital del anterior volvió al
banco. Las capturas no se cuentan como operaciones independientes.

Ciclo:
  1. en la captura t, elegir el anuncio P2P más barato que pase los filtros
     (medios de pago del usuario, contraparte, límites) y cuyo margen
     esperado contra el bid ACTUAL supere el umbral de entrada
  2. pagar (demora pay_s) y esperar la liberación (release_s)
  3. vender en la PRIMERA captura posterior a t + pay_s + release_s,
     recorriendo los niveles del libro (deslizamiento real); comisión spot
  4. retirar ARS (comisión y demora de retiro: escenarios, dato no público)

Rendimiento neto (%) = (ARS finales − ARS pagados) / ARS pagados × 100
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

# Costos con su estado (ver informe). Los escenarios se pasan en Costs.
SPOT_TAKER_VERIFIED = 0.001        # VERIFICADO: binance.com/en/fee/trading, usuario regular 0,100%
SPOT_TAKER_BNB = 0.00075           # VERIFICADO: misma página, con BNB 0,075%


@dataclass
class Costs:
    p2p_taker: float = 0.0          # PUBLICADO (anuncio 2021 / Binance Square): tomador 0%; no verificado en la cuenta
    spot_taker: float = SPOT_TAKER_VERIFIED
    ars_withdraw_pct: float = 0.0   # DESCONOCIDO: no público; escenarios
    ars_withdraw_fixed: float = 0.0 # DESCONOCIDO
    withdraw_s: float = 15 * 60     # DESCONOCIDO: demora hasta tener los ARS en el banco


@dataclass
class Policy:
    capital_ars: float = 500_000
    usable_methods: List[str] = field(default_factory=lambda: ["BankArgentina", "NaranjaX", "MercadoPagoNew"])
    counterparty: str = "merchant"  # "any" | "merchant" | "solid" (comerciante o >=100 órdenes/mes y >=98%)
    min_edge: float = 0.0005        # margen esperado mínimo para entrar (después de costos conocidos)
    pay_s: float = 180              # SUPUESTO: transferir y marcar pagado
    release_s: float = 97           # OBSERVADO: mediana de liberación de comerciantes (perfiles, 15/10)


def _ts(x):
    return datetime.fromisoformat(x.replace("Z", "+00:00"))


def passes(ad, pol: Policy):
    if not set(ad.get("methods") or []) & set(pol.usable_methods):
        return False
    if pol.counterparty == "merchant":
        return ad.get("user_type") == "merchant"
    if pol.counterparty == "solid":
        return ad.get("user_type") == "merchant" or (
            (ad.get("orders_month") or 0) >= 100 and (ad.get("finish_rate") or 0) >= 0.98)
    return True


def sell_book(bids, usdt, fee):
    left, ars = usdt, 0.0
    for p, q in bids:
        t = min(left, q)
        ars += t * p
        left -= t
        if left <= 1e-9:
            break
    return ars * (1 - fee), usdt - left


def expected_edge(price, bid, costs: Costs):
    return bid * (1 - costs.spot_taker) * (1 - costs.ars_withdraw_pct) / (price * (1 + costs.p2p_taker)) - 1


def pick(snap, pol: Policy, costs: Costs):
    bids = _bids(snap)
    if not bids:
        return None
    best = None
    for ad in (snap.get("p2p_usdt_ars_buy") or {}).get("data") or []:
        if not passes(ad, pol):
            continue
        amount = min(pol.capital_ars, ad["max_ars"], ad["qty"] * ad["price"])
        if amount < ad["min_ars"] or amount <= 0:
            continue
        edge = expected_edge(ad["price"], bids[0][0], costs)
        if edge < pol.min_edge:
            continue
        if best is None or ad["price"] < best[0]["price"]:
            best = (ad, amount, edge)
    return best


def _bids(snap):
    d = (snap.get("binance_usdtars") or {}).get("data") or {}
    return [(float(p), float(q)) for p, q in d.get("bids", [])]


def run(snaps, pol: Policy, costs: Costs, max_gap_s=180):
    """-> lista de ciclos simulados (secuenciales). Un ciclo cuya venta cae
    en un hueco de datos (> max_gap_s sin captura) se marca SIN_DATOS: no se
    inventa el precio."""
    snaps = sorted(snaps, key=lambda s: s["ts"])
    times = [_ts(s["ts"]) for s in snaps]
    cycles, free_at, i = [], None, 0
    while i < len(snaps):
        t0 = times[i]
        if free_at and t0 < free_at:
            i += 1
            continue
        p = pick(snaps[i], pol, costs)
        if not p:
            i += 1
            continue
        ad, amount, edge = p
        sell_at = t0 + timedelta(seconds=pol.pay_s + pol.release_s)
        j = next((k for k in range(i, len(snaps)) if times[k] >= sell_at), None)
        if j is None or (times[j] - sell_at).total_seconds() > max_gap_s:
            cycles.append({"ts": snaps[i]["ts"], "status": "SIN_DATOS"})
            i += 1
            continue
        usdt = amount / ad["price"] / (1 + costs.p2p_taker)
        ars, sold = sell_book(_bids(snaps[j]), usdt, costs.spot_taker)
        if sold < usdt - 1e-6:
            cycles.append({"ts": snaps[i]["ts"], "status": "SIN_PROFUNDIDAD"})
            i += 1
            continue
        ars_final = ars * (1 - costs.ars_withdraw_pct) - costs.ars_withdraw_fixed
        sold_ts = times[j]
        back = sold_ts + timedelta(seconds=costs.withdraw_s)
        cycles.append({
            "ts": snaps[i]["ts"], "sold_ts": snaps[j]["ts"], "status": "OK",
            "ad_price": ad["price"], "user_type": ad.get("user_type"), "methods": ad.get("methods"),
            "ars_paid": amount, "usdt": usdt, "bid_at_decision": _bids(snaps[i])[0][0],
            "avg_sell": (ars / (1 - costs.spot_taker)) / usdt, "expected_edge": edge,
            "net_ars": ars_final - amount, "net_pct": (ars_final - amount) / amount * 100,
            "price_move_pct": ((ars / (1 - costs.spot_taker)) / usdt / _bids(snaps[i])[0][0] - 1) * 100,
            "cycle_s": (back - t0).total_seconds()})
        free_at = back
        i = j
    return cycles


def summarize(cycles, hours_observed):
    ok = [c for c in cycles if c["status"] == "OK"]
    if not ok:
        return {"cycles": 0, "other": len(cycles) - len(ok)}
    net = sorted(c["net_pct"] for c in ok)
    n = len(net)
    return {"cycles": n, "other_status": len(cycles) - n,
            "positive": sum(x > 0 for x in net), "positive_share": sum(x > 0 for x in net) / n,
            "net_pct_p10": net[int(0.1 * (n - 1))], "net_pct_median": net[n // 2], "net_pct_min": net[0],
            "net_pct_max": net[-1], "net_ars_total": sum(c["net_ars"] for c in ok),
            "ars_paid_median": sorted(c["ars_paid"] for c in ok)[n // 2],
            "ars_paid_max": max(c["ars_paid"] for c in ok),
            "cycle_min_median": sorted(c["cycle_s"] for c in ok)[n // 2] / 60,
            "worst_price_move_pct": min(c["price_move_pct"] for c in ok),
            "cycles_per_hour": n / hours_observed if hours_observed else None,
            "net_ars_per_hour": sum(c["net_ars"] for c in ok) / hours_observed if hours_observed else None}
