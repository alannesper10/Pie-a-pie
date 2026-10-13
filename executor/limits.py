"""Límites propios de Pie a Pie. Ninguna orden de HORUS puede superarlos: se
aplica el más restrictivo entre la orden y config/executor_limits.json."""

import json
from pathlib import Path

LIMITS_FILE = Path("config") / "executor_limits.json"


def load_limits(path=LIMITS_FILE):
    with open(path, encoding="utf-8") as f:
        lim = json.load(f)
    if lim.get("paper_only") is not True:
        raise SystemExit("executor_limits.json debe tener paper_only=true")
    return lim


def check_order(order, limits, ledger, ref_price):
    """-> lista de (código, detalle). ref_price: mejor precio contrario actual
    (para pasar qty a USD y estimar la pérdida máxima)."""
    out = []
    ins = order["instrument"]
    if ins["asset_class"] not in limits["asset_classes"]:
        out.append(("ASSET_CLASS_NOT_SUPPORTED", ins["asset_class"]))
    bad = [v for v in ins["venues_allowed"] if v not in limits["venues"]]
    if bad:
        out.append(("VENUE_NOT_ALLOWED", bad))
    sz = order["sizing"]
    notional = sz.get("notional_usd") or ((sz.get("qty") or 0) * (ref_price or 0))
    if not ref_price and sz.get("qty"):
        out.append(("DATA_UNAVAILABLE", "sin precio de referencia para valuar qty"))
    if notional > limits["max_notional_per_order_usd"] + 1e-9:
        out.append(("LIMIT_NOTIONAL", {"notional": notional, "max": limits["max_notional_per_order_usd"]}))
    max_pos = (order.get("risk") or {}).get("max_position_usd")
    if max_pos is not None and notional > max_pos + 1e-9:
        out.append(("LIMIT_NOTIONAL", {"notional": notional, "max_position_usd": max_pos}))
    if order["direction"] == "buy":
        if ledger.exposure_usd() + notional > limits["max_total_exposure_usd"] + 1e-9:
            out.append(("LIMIT_EXPOSURE", {"exposure": ledger.exposure_usd(), "add": notional,
                                           "max": limits["max_total_exposure_usd"]}))
        if notional > ledger.cash + 1e-9:
            out.append(("INSUFFICIENT_CAPITAL", {"cash": ledger.cash, "need": notional}))
        # Pérdida máxima: con stop, hasta el stop (+ comisiones); sin stop, todo el nocional.
        stop = (order.get("exit") or {}).get("stop")
        if stop and ref_price:
            worst = notional * max(0.0, 1 - stop / ref_price) + notional * 0.004
        else:
            worst = notional
        cap = min(order["risk"]["max_loss_usd"], limits["max_loss_per_order_usd"])
        if worst > cap + 1e-9:
            out.append(("LIMIT_LOSS", {"worst_case_usd": round(worst, 6), "max_loss_usd": cap,
                                       "stop": stop}))
    else:
        base = ins["symbol"].split("/")[0]
        qty = sz.get("qty") or (notional / ref_price if ref_price else 0)
        if ledger.inventory(base) + 1e-12 < qty:
            out.append(("INSUFFICIENT_INVENTORY", {"have": ledger.inventory(base), "need": qty}))
    return out
