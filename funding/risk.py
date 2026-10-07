"""Riesgo de spot largo + perp corto (puro)."""

COUNTERPARTY_NOTE = {
    "binance": "exchange centralizado; custodia en el exchange",
    "bybit": "exchange centralizado; custodia en el exchange",
    "okx": "exchange centralizado; custodia en el exchange",
}


def capital_required(notional, leverage):
    """Spot comprado (N) + margen del perp corto (N / L)."""
    return notional + notional / leverage


def short_liquidation_price(entry, leverage, maintenance_margin):
    """Precio de liquidación aprox. de un short con margen aislado N/L.

    Liquida cuando la pérdida (F - F0)/F0 alcanza 1/L - mmr.
    """
    return entry * (1.0 + 1.0 / leverage - maintenance_margin)


def liquidation_distance(price, liq_price):
    """Cuánto puede subir el precio (fracción) antes de liquidar."""
    return (liq_price - price) / price if price else 0.0


def risk_flags(*, expected_rate, trailing_rate, basis_pct, liq_distance,
               depth_ok, exchange):
    return {
        "riesgo_funding_negativo": trailing_rate < 0 or expected_rate < 0,
        "riesgo_basis_contrario": basis_pct < 0,
        "riesgo_liquidacion": liq_distance < 0.25,
        "riesgo_ejecucion": not depth_ok,
        "riesgo_contraparte": COUNTERPARTY_NOTE.get(exchange, "desconocido"),
    }
