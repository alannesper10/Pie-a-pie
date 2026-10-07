"""Configuración de funding/basis. Cada costo lleva su estado de verificación.

VERIFIED   = leído de una fuente pública en este código (API, libro, historial).
ASSUMED    = valor razonable tomado de tarifas públicas estándar, NO verificado
             para una cuenta concreta. Hay que confirmarlo antes de dinero real.
UNVERIFIED = no se pudo obtener (endpoint con autenticación, error, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict

VERIFIED, ASSUMED, UNVERIFIED = "VERIFIED", "ASSUMED", "UNVERIFIED"

PAPER_ONLY = True     # condición obligatoria; no hay código de órdenes reales


@dataclass(frozen=True)
class Param:
    value: float
    status: str
    source: str


# Tarifas taker/maker de nivel base publicadas por cada exchange. Las APIs de
# tarifas por cuenta requieren autenticación, así que quedan como ASSUMED.
_STD = "tarifa pública estándar de nivel base; no verificada por cuenta"
DEFAULT_FEES: Dict[str, Dict[str, Param]] = {
    "binance": {
        "spot_taker": Param(0.0010, ASSUMED, _STD),
        "spot_maker": Param(0.0010, ASSUMED, _STD),
        "perp_taker": Param(0.0005, ASSUMED, _STD),
        "perp_maker": Param(0.0002, ASSUMED, _STD),
    },
    "bybit": {
        "spot_taker": Param(0.0010, ASSUMED, _STD),
        "spot_maker": Param(0.0010, ASSUMED, _STD),
        "perp_taker": Param(0.00055, ASSUMED, _STD),
        "perp_maker": Param(0.0002, ASSUMED, _STD),
    },
    "okx": {
        "spot_taker": Param(0.0010, ASSUMED, _STD),
        "spot_maker": Param(0.0008, ASSUMED, _STD),
        "perp_taker": Param(0.0005, ASSUMED, _STD),
        "perp_maker": Param(0.0002, ASSUMED, _STD),
    },
}


@dataclass(frozen=True)
class FundingConfig:
    exchanges: tuple = ("binance", "bybit", "okx")
    assets: tuple = ("BTC", "ETH", "SOL")
    quote: str = "USDT"

    starting_capital_usd: float = 100.0
    allocation: float = 0.90         # 10% de reserva para rebalanceo/costos
    leverage: float = 1.0            # 1x por defecto; no se maximiza

    # Costos y ejecución (ASSUMED salvo que se mida en vivo)
    extra_slippage: Param = Param(0.0002, ASSUMED, "slippage extra por pata y por operación")
    latency_ms: Param = Param(500.0, ASSUMED, "latencia entre decisión y llegada de la orden")
    leg_fail_prob: Param = Param(0.02, ASSUMED, "prob. de que la segunda pata no se ejecute")
    unmatched_penalty: Param = Param(0.0010, ASSUMED, "costo extra al deshacer/cubrir una pata despareja")
    maintenance_margin: Param = Param(0.005, ASSUMED, "margen de mantenimiento aprox. del primer tramo")
    rebalance_threshold: Param = Param(0.50, ASSUMED, "rebalancear cuando la pérdida del perp supera este % del margen")
    transfer_cost_usd: Param = Param(0.0, ASSUMED, "mismo exchange: sin transferencias")
    counterparty_haircut: Param = Param(0.0, ASSUMED, "no se descuenta; se registra como riesgo cualitativo")

    # Regla de decisión (sin mirar el futuro)
    horizon_days: float = 7.0
    trailing_periods: int = 3
    max_hold_days: float = 30.0
    history_days: int = 90

    fees: Dict[str, Dict[str, Param]] = field(default_factory=lambda: DEFAULT_FEES)

    def fee(self, exchange, key):
        return self.fees[exchange][key]

    def notional_for_capital(self, capital=None):
        """Nocional por pata que entra en el capital: spot N + margen N/L."""
        capital = self.starting_capital_usd if capital is None else capital
        return capital * self.allocation / (1.0 + 1.0 / self.leverage)


def effective_fees(cfg_fees: Dict[str, Param], ccxt_spot_taker, ccxt_perp_taker):
    """Comisión efectiva = la MAYOR entre la configurada y la de referencia de
    ccxt (ambas ASSUMED). Conservador ante la duda."""
    out = dict(cfg_fees)
    for key, ref in (("spot_taker", ccxt_spot_taker), ("perp_taker", ccxt_perp_taker)):
        base = cfg_fees[key]
        if ref is not None and float(ref) > base.value:
            out[key] = Param(float(ref), ASSUMED,
                             f"máx(config {base.value:.4%}, ccxt {float(ref):.4%}); no verificada por cuenta")
        else:
            out[key] = Param(base.value, ASSUMED,
                             f"máx(config {base.value:.4%}, ccxt "
                             f"{'n/d' if ref is None else f'{float(ref):.4%}'}); no verificada por cuenta")
    return out
