"""Simulador de la ruta dólar oficial -> USDT/USDC -> ARS (solo investigación).

Reconstruye el ciclo completo desde los ARS iniciales hasta los ARS finales
con precios EJECUTABLES y sus límites:

  1. ARS -> USD en el banco o billetera (precio de venta al público del banco)
  2. USD -> plataforma (transferencia; costo y demora por ruta)
  3. USD -> USDT: anuncios P2P (precio en USD por USDT, cantidad y mínimo y
     máximo por orden) o la cotización de una plataforma que reciba USD
  4. USDT -> ARS: libro spot de Binance (recorriendo niveles) o anuncios P2P
  5. retiro de ARS

Rendimiento neto (%) = (ARS finales − ARS iniciales) / ARS iniciales × 100

No consulta APIs, no opera, no usa claves: recibe precios ya capturados
(lab/research/fx_capture.py) y devuelve el detalle de cada paso. Cada
parámetro de costo lleva su estado en COSTS (VERIFICADO / PUBLICADO /
SUPUESTO / NO_VERIFICADO); el resultado nunca es "rentable" por sí solo: es
una simulación con esos supuestos.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

COSTS = {
    "bank_purchase_fee": (0.0, "NO_VERIFICADO: compra online sin comisión explícita; el costo está en el precio de venta"),
    "local_usd_transfer_fee_usd": (0.0, "PUBLICADO (Naranja X: transferencias en USD entre cuentas argentinas gratis); BNA NO_VERIFICADO"),
    "p2p_taker_fee": (0.0, "NO_VERIFICADO: Binance P2P sin comisión para el tomador del anuncio"),
    "binance_spot_taker": (0.001, "PUBLICADO: tarifa estándar spot 0,10% (no verificada para la cuenta)"),
    "ars_withdraw_fee": (0.0, "NO_VERIFICADO"),
}


def cost(name):
    return COSTS[name][0]


@dataclass
class Ad:
    """Anuncio P2P. price en fiat por USDT; qty en USDT; min/max por orden en fiat."""
    price: float
    qty: float
    min_fiat: float
    max_fiat: float
    methods: List[str] = field(default_factory=list)
    user_type: Optional[str] = None
    finish_rate: Optional[float] = None


def take_ads_buy(ads: List[Ad], fiat: float, usable_methods=None):
    """Comprar USDT gastando `fiat` en anuncios ordenados por precio (más barato primero).
    Respeta mínimo/máximo por orden, la cantidad disponible y los medios de pago
    que el usuario puede usar. -> (usdt, fiat_gastado, órdenes)"""
    left, usdt, orders = fiat, 0.0, []
    for a in sorted(ads, key=lambda a: a.price):
        if usable_methods is not None and not set(a.methods) & set(usable_methods):
            continue
        cap = min(a.max_fiat, a.qty * a.price, left)
        if cap < a.min_fiat or cap <= 0:
            continue
        usdt += cap / a.price
        left -= cap
        orders.append({"price": a.price, "fiat": cap, "usdt": cap / a.price, "methods": a.methods})
        if left <= 1e-9:
            break
    return usdt, fiat - left, orders


def take_ads_sell(ads: List[Ad], usdt: float, usable_methods=None):
    """Vender `usdt` en anuncios de compra (mejor precio primero). -> (fiat, usdt_vendido, órdenes)"""
    left, fiat, orders = usdt, 0.0, []
    for a in sorted(ads, key=lambda a: -a.price):
        if usable_methods is not None and not set(a.methods) & set(usable_methods):
            continue
        q = min(left, a.qty, a.max_fiat / a.price)
        if q * a.price < a.min_fiat or q <= 0:
            continue
        fiat += q * a.price
        left -= q
        orders.append({"price": a.price, "usdt": q, "fiat": q * a.price})
        if left <= 1e-9:
            break
    return fiat, usdt - left, orders


def take_book_sell(bids, usdt: float):
    """Vender `usdt` contra los bids [(precio, cantidad)]. -> (ars_bruto, usdt_vendido)"""
    left, ars = usdt, 0.0
    for p, q in bids:
        t = min(left, q)
        ars += t * p
        left -= t
        if left <= 1e-12:
            break
    return ars, usdt - left


@dataclass
class Route:
    name: str
    bank: str
    bank_ask: float                       # ARS por USD (venta al público)
    usd_to_usdt: str                      # "p2p" o "platform"
    usable_methods: Optional[List[str]] = None
    platform_usdt_ask: Optional[float] = None   # USD por USDT (plataforma que recibe USD)
    sell_on: str = "binance_spot"         # "binance_spot" o "p2p"
    hours: tuple = (None, None)           # demora estimada (mín, máx) del ciclo, en horas
    notes: str = ""


def simulate(route: Route, ars0: float, usd_ads=None, ars_sell_ads=None, binance_bids=None):
    out = {"route": route.name, "ars0": ars0, "status": "OK", "steps": {}}
    usd = ars0 * (1 - cost("bank_purchase_fee")) / route.bank_ask
    out["steps"]["usd_bought"] = usd
    usd -= cost("local_usd_transfer_fee_usd")
    if route.usd_to_usdt == "p2p":
        usdt, spent, orders = take_ads_buy(usd_ads or [], usd, route.usable_methods)
        usdt *= 1 - cost("p2p_taker_fee")
        out["steps"]["p2p_buy_orders"] = orders
        if spent < usd - 1e-6:
            out["status"] = "SIN_LIQUIDEZ_O_LIMITES"         # no se pudo convertir todo: no se inventa
            out["steps"]["usd_unconverted"] = usd - spent
    else:
        if not route.platform_usdt_ask:
            return {**out, "status": "SIN_PRECIO"}
        usdt = usd / route.platform_usdt_ask
    out["steps"]["usdt"] = usdt
    if route.sell_on == "binance_spot":
        ars, sold = take_book_sell(binance_bids or [], usdt)
        ars *= 1 - cost("binance_spot_taker")
    else:
        ars, sold, orders = take_ads_sell(ars_sell_ads or [], usdt)
        out["steps"]["p2p_sell_orders"] = orders
    if sold < usdt - 1e-6:
        out["status"] = "SIN_LIQUIDEZ_O_LIMITES"
        out["steps"]["usdt_unsold"] = usdt - sold
    ars *= 1 - cost("ars_withdraw_fee")
    out["ars_final"] = ars
    out["pnl_ars"] = ars - ars0 if out["status"] == "OK" else None
    out["net_pct"] = (ars - ars0) / ars0 * 100 if out["status"] == "OK" else None
    h0, h1 = route.hours
    if out["net_pct"] is not None and h1:
        out["net_pct_per_day_worst"] = out["net_pct"] / max(h1 / 24, 1)   # un ciclo por día como máximo
    if usdt and sold:
        # precio medio de venta obtenido y el máximo USD/USDT que se podía pagar sin perder
        out["avg_sell_ars_per_usdt"] = ars / sold
        out["breakeven_usd_per_usdt"] = (ars / sold) / route.bank_ask
        out["paid_usd_per_usdt"] = usd / usdt
    return out


def breakeven_usd_per_usdt(bank_ask, usdt_bid_ars, spot_fee=None):
    """Máximo precio (USD por USDT) que se puede pagar para no perder:
    usdt_bid*(1-fee) / bank_ask."""
    fee = cost("binance_spot_taker") if spot_fee is None else spot_fee
    return usdt_bid_ars * (1 - fee) / bank_ask


def ads_from_capture(rows) -> List[Ad]:
    return [Ad(price=r["price"], qty=r["qty"], min_fiat=r["min_ars"], max_fiat=r["max_ars"],
               methods=r.get("methods") or [], user_type=r.get("user_type"), finish_rate=r.get("finish_rate"))
            for r in rows or []]
