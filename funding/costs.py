"""Modelo explícito de costos de spot largo + perp corto (puro).

Todo en fracción del nocional por pata, salvo que se indique USD. Cada
componente se informa por separado con su estado (VERIFIED/ASSUMED/...).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .config import ASSUMED, VERIFIED, FundingConfig, Param


def walk_book(levels: List[Tuple[float, float]], qty: float):
    """Barre niveles [(precio, cantidad)] para `qty`. Soporta fill parcial.

    Devuelve (cantidad_llenada, precio_promedio, costo_total).
    """
    filled = cost = 0.0
    for price, size in levels:
        if filled >= qty - 1e-15:
            break
        take = min(size, qty - filled)
        filled += take
        cost += take * price
    avg = cost / filled if filled else 0.0
    return filled, avg, cost


def slippage_vs_mid(levels, qty, mid, side):
    """Slippage (fracción) de barrer el libro respecto del mid. None si no llena."""
    filled, avg, _ = walk_book(levels, qty)
    if filled < qty - 1e-12 or not mid:
        return None
    return (avg - mid) / mid if side == "buy" else (mid - avg) / mid


@dataclass
class CostBreakdown:
    """Costos de ida y vuelta (entrada + salida) como fracción del nocional."""
    items: Dict[str, Param] = field(default_factory=dict)

    def add(self, name, value, status, source):
        self.items[name] = Param(value, status, source)

    @property
    def total(self):
        return sum(p.value for p in self.items.values())

    def statuses(self):
        return {k: p.status for k, p in self.items.items()}

    def as_dict(self):
        return {k: {"value": p.value, "status": p.status, "source": p.source}
                for k, p in self.items.items()}


def round_trip_costs(cfg: FundingConfig, exchange, *, spot_half_spread=None,
                     perp_half_spread=None, spot_depth_slip=None,
                     perp_depth_slip=None, expected_rebalances=0.0,
                     transfers=0) -> CostBreakdown:
    """Costos de entrar y salir (4 operaciones taker) + rebalanceo + transferencias.

    Spread y slippage por profundidad: VERIFIED si vienen de un libro real,
    si no ASSUMED (se usa el slippage extra configurado).
    """
    c = CostBreakdown()
    st, pt = cfg.fee(exchange, "spot_taker"), cfg.fee(exchange, "perp_taker")
    c.add("fee_spot_entrada", st.value, st.status, st.source)
    c.add("fee_spot_salida", st.value, st.status, st.source)
    c.add("fee_perp_entrada", pt.value, pt.status, pt.source)
    c.add("fee_perp_salida", pt.value, pt.status, pt.source)

    for leg, half, slip in (("spot", spot_half_spread, spot_depth_slip),
                            ("perp", perp_half_spread, perp_depth_slip)):
        if half is not None:
            c.add(f"spread_{leg}", 2 * half, VERIFIED, "libro actual (entrada + salida)")
        else:
            c.add(f"spread_{leg}", 0.0, ASSUMED, "sin libro: incluido en slippage extra")
        if slip is not None:
            c.add(f"slippage_profundidad_{leg}", 2 * slip, VERIFIED,
                  "barrido del libro actual para el tamaño")
    es = cfg.extra_slippage
    c.add("slippage_extra", 4 * es.value, es.status, es.source)

    if expected_rebalances:
        per = st.value + pt.value + 2 * es.value
        c.add("rebalanceo", expected_rebalances * per, ASSUMED,
              "fees+slippage sobre el monto rebalanceado (aprox.)")
    tc = cfg.transfer_cost_usd
    c.add("transferencias", transfers * tc.value, tc.status, tc.source)
    return c


def rebalance_cost_usd(amount_usd, cfg: FundingConfig, exchange):
    """Costo de mover `amount_usd` de spot a margen manteniendo delta neutral:
    vender spot y achicar el short por el mismo monto (2 operaciones)."""
    st, pt = cfg.fee(exchange, "spot_taker"), cfg.fee(exchange, "perp_taker")
    return amount_usd * (st.value + pt.value + 2 * cfg.extra_slippage.value)


def breakeven_periods(round_trip_cost, rate_per_period) -> Optional[float]:
    """Períodos de funding necesarios para recuperar los costos (None si rate <= 0)."""
    if rate_per_period <= 0:
        return None
    return round_trip_cost / rate_per_period
