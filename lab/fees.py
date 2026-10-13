"""Costos del laboratorio con estado de verificación.

Las tarifas por cuenta requieren claves en todos los exchanges (verificado:
AuthenticationError / NotSupported), así que las comisiones de trading y de
retiro son ASSUMED. Se usa la MAYOR entre la tarifa pública de nivel base y la
referencia de ccxt (conservador). Polymarket publica su tasa por mercado en
`feeSchedule` (VERIFIED desde la API).
"""

from .core import ASSUMED, VERIFIED, Cost

# Tarifas públicas de nivel base (taker, maker) — ASSUMED, no verificadas por cuenta.
BASE_FEES = {
    "binance": (0.0010, 0.0010),
    "bybit": (0.0010, 0.0010),
    "okx": (0.0010, 0.0008),
    "kraken": (0.0040, 0.0025),
    "coinbase": (0.0120, 0.0060),
}

# Costo de retiro/rebalanceo por transferencia, en USD — ASSUMED (las APIs de
# fees de retiro piden claves o no están soportadas).
WITHDRAW_USD = {"BTC": 10.0, "ETH": 3.0, "SOL": 0.5, "USDT": 1.0}
TRADES_PER_REBALANCE = 10        # el inventario se rebalancea cada N operaciones


def taker_fee(venue, ccxt_ref=None):
    base = BASE_FEES.get(venue, (0.0050, 0.0050))[0]
    rate = max(base, float(ccxt_ref)) if ccxt_ref is not None else base
    return rate, f"máx(tarifa base {base:.4%}, ccxt {ccxt_ref}); no verificada por cuenta"


def maker_fee(venue, ccxt_ref=None):
    base = BASE_FEES.get(venue, (0.0050, 0.0050))[1]
    rate = max(base, float(ccxt_ref)) if ccxt_ref is not None else base
    return rate, f"máx(tarifa base {base:.4%}, ccxt {ccxt_ref}); no verificada por cuenta"


def fee_cost(notional_usd, venue, ccxt_ref=None, maker=False):
    rate, src = (maker_fee if maker else taker_fee)(venue, ccxt_ref)
    return Cost(notional_usd * rate, ASSUMED, src)


def transfer_cost(asset):
    usd = WITHDRAW_USD.get(asset, 5.0) / TRADES_PER_REBALANCE
    return Cost(usd, ASSUMED, f"retiro {asset} ~US${WITHDRAW_USD.get(asset, 5.0)} "
                f"amortizado en {TRADES_PER_REBALANCE} operaciones")


def polymarket_fee(shares, price, fee_schedule):
    """fee = C x rate x p x (1-p) (centro de ayuda de Polymarket, 10/07/2026).

    La variante con exponente que citan terceros da un valor menor o igual, así
    que esta es la conservadora. Solo pagan los takers.
    """
    if not fee_schedule:
        return Cost(shares * 0.05 * price * (1 - price), ASSUMED,
                    "sin feeSchedule: tasa 0.05 supuesta")
    rate = float(fee_schedule.get("rate") or 0.0)
    return Cost(round(shares * rate * price * (1 - price), 5), VERIFIED,
                f"feeSchedule.rate={rate} de la API; fórmula C*rate*p*(1-p)")
