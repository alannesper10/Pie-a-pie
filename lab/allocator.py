"""Asignación dinámica de capital entre estrategias habilitadas (familia 6).

Regla: una estrategia recibe capital SOLO si pasa la misma compuerta de
evidencia que el veredicto RENTABLE del laboratorio (lab/evaluate:
≥30 ejecuciones, ≥6 períodos, fuera de muestra > 0, estrés de costos > 0,
≥60% de períodos positivos y P&L realizado). Sin evidencia: 0, aunque el
retorno estimado sea alto. Los umbrales están congelados aquí y no se
ajustan para producir asignaciones.

Entre las que pasan, el peso es proporcional al retorno neto por unidad de
capital y de tiempo bloqueado, dividido por la pérdida máxima relativa, con
tope por la capacidad (liquidez) y por una participación máxima.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .evaluate import MIN_PERIODS, MIN_POSITIVE_PERIODS, MIN_TRADES

MAX_SHARE = 0.40            # ninguna estrategia recibe más del 40% del capital
RESERVE = 0.10              # 10% siempre sin asignar (margen, imprevistos)


@dataclass
class StrategyEvidence:
    name: str
    realized_trades: int
    periods: int
    positive_period_share: float
    net_return_per_capital_day: float     # realizado, no estimado
    oos_net: float
    stress_net: float
    max_loss_fraction: float              # pérdida máxima / capital comprometido
    capacity_usd: float                   # cuánto admite la liquidez observada
    enabled: bool = True                  # el usuario/HORUS puede deshabilitar


def gate(e: StrategyEvidence) -> List[str]:
    """Motivos por los que NO recibe capital (vacío = pasa)."""
    why = []
    if not e.enabled:
        why.append("deshabilitada")
    if e.realized_trades < MIN_TRADES:
        why.append(f"{e.realized_trades} operaciones realizadas (mín {MIN_TRADES})")
    if e.periods < MIN_PERIODS:
        why.append(f"{e.periods} períodos (mín {MIN_PERIODS})")
    if e.positive_period_share < MIN_POSITIVE_PERIODS:
        why.append(f"{e.positive_period_share:.0%} períodos positivos (mín {MIN_POSITIVE_PERIODS:.0%})")
    if e.oos_net <= 0:
        why.append("fuera de muestra <= 0")
    if e.stress_net <= 0:
        why.append("no resiste costos x1,5")
    if e.net_return_per_capital_day <= 0:
        why.append("retorno realizado <= 0")
    return why


def allocate(capital: float, evidence: List[StrategyEvidence]) -> Dict[str, dict]:
    out, scores = {}, {}
    for e in evidence:
        why = gate(e)
        out[e.name] = {"allocated_usd": 0.0, "eligible": not why, "reasons": why}
        if not why:
            scores[e.name] = e.net_return_per_capital_day / max(e.max_loss_fraction, 1e-6)
    budget = capital * (1 - RESERVE)
    total = sum(scores.values())
    if total <= 0:
        return out
    by = {e.name: e for e in evidence}
    left = budget
    for name, s in sorted(scores.items(), key=lambda x: -x[1]):
        amt = min(budget * s / total, capital * MAX_SHARE, by[name].capacity_usd, left)
        out[name]["allocated_usd"] = amt
        out[name]["capped_by"] = [k for k, v in (("participación", capital * MAX_SHARE),
                                                 ("capacidad", by[name].capacity_usd)) if amt >= v - 1e-9]
        left -= amt
    return out
