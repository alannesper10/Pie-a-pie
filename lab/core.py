"""Motor común de simulación del laboratorio.

Tres niveles de evidencia, siempre separados en cada oportunidad:
  OBSERVED  = precios/tamaños leídos de una fuente pública (sin supuestos).
  ESTIMATED = neto calculado sobre lo observado + costos modelados.
  SIMULATED = resultado de simular la ejecución (latencia, fills parciales,
              pata fallida, oportunidad desaparecida, liquidez ya usada).
"""

import math
import random
import threading
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

from . import PAPER_ONLY

VERIFIED, ASSUMED, UNVERIFIED = "VERIFIED", "ASSUMED", "UNVERIFIED"
ACCEPTED, REJECTED = "ACCEPTED", "REJECTED"

Levels = List[Tuple[float, float]]   # [(precio, cantidad)] mejor primero


# ------------------------------------------------------------------ costos ---

@dataclass(frozen=True)
class Cost:
    usd: float
    status: str
    source: str


def cost_total(costs: Dict[str, Cost]) -> float:
    return sum(c.usd for c in costs.values())


def scale_costs(costs: Dict[str, Cost], factor: float) -> float:
    """Costos totales con un factor de estrés (fees, spread, slippage...)."""
    return sum(c.usd * factor for c in costs.values())


# ------------------------------------------------------------- oportunidad ---

@dataclass
class Opportunity:
    strategy: str
    key: str                      # identidad estable de la oportunidad (rachas/dedup)
    tick: int
    ts: str
    venues: List[str]
    instruments: List[str]
    observed: dict                # precios crudos, tamaños, timestamps de origen
    gross_usd: float = 0.0        # ganancia bruta estimada (antes de costos)
    costs: Dict[str, Cost] = field(default_factory=dict)
    capital_usd: float = 0.0      # capital comprometido por la oportunidad
    size: float = 0.0             # tamaño estimado ejecutable (unidades del módulo)
    stage: str = "OBSERVED"       # hasta qué nivel de evidencia llegó
    decision: str = REJECTED
    reason: str = ""
    assumptions: List[str] = field(default_factory=list)
    sim: Optional[dict] = None    # resultado de la simulación de ejecución
    uid: str = ""                 # lo asigna el runner al guardar (re-guardado idempotente)
    classification: str = ""      # ver src/guarantee.CATEGORIES
    classification_reason: str = ""
    lock_hours: Optional[float] = None   # cuánto queda bloqueado el capital (None = instantáneo/desconocido)
    max_loss_usd: Optional[float] = None # pérdida posible en el peor escenario modelado
    valid_until: Optional[str] = None    # vigencia conocida (vencimiento, cierre del mercado)
    final_result: Optional[dict] = None  # resultado verificado ex post (liquidación real)

    @property
    def net_estimated_usd(self):
        return self.gross_usd - cost_total(self.costs)

    @property
    def net_estimated_pct(self):
        return self.net_estimated_usd / self.capital_usd if self.capital_usd else 0.0

    @property
    def net_simulated_usd(self):
        return None if not self.sim else self.sim.get("net_usd")

    @property
    def costs_verified_usd(self):
        return sum(c.usd for c in self.costs.values() if c.status == VERIFIED)

    @property
    def costs_assumed_usd(self):
        return sum(c.usd for c in self.costs.values() if c.status != VERIFIED)

    def to_row(self):
        d = asdict(self)
        d["costs"] = {k: asdict(v) for k, v in self.costs.items()}
        d["net_estimated_usd"] = self.net_estimated_usd
        d["net_estimated_pct"] = self.net_estimated_pct
        d["costs_verified_usd"] = self.costs_verified_usd
        d["costs_assumed_usd"] = self.costs_assumed_usd
        return d


# ----------------------------------------------- liquidez compartida (dedup) ---

class LiquidityRegistry:
    """Evita que dos estrategias consuman la misma liquidez en el mismo tick.

    Cada (venue, símbolo, lado, precio) tiene una cantidad disponible; lo que
    una estrategia reclama ya no está para la siguiente. Se reinicia por tick.
    """

    def __init__(self):
        self._used: Dict[tuple, float] = {}
        self._lock = threading.Lock()

    def available(self, venue, symbol, side, levels: Levels) -> Levels:
        with self._lock:
            out = []
            for p, q in levels:
                left = q - self._used.get((venue, symbol, side, p), 0.0)
                if left > 1e-12:
                    out.append((p, left))
            return out

    def claim(self, venue, symbol, side, fills: Levels):
        with self._lock:
            for p, q in fills:
                k = (venue, symbol, side, p)
                self._used[k] = self._used.get(k, 0.0) + q


# ----------------------------------------------------------- ejecución sim ---

def walk(levels: Levels, qty: float):
    """Barre niveles para `qty`. -> (llenado, costo_total, fills)."""
    filled = cost = 0.0
    fills = []
    for p, q in levels:
        if filled >= qty - 1e-15:
            break
        take = min(q, qty - filled)
        filled += take
        cost += take * p
        fills.append((p, take))
    return filled, cost, fills


def walk_quote(levels: Levels, quote_amount: float):
    """Gasta `quote_amount` comprando contra asks. -> (base_obtenida, gastado, fills)."""
    base = spent = 0.0
    fills = []
    for p, q in levels:
        if spent >= quote_amount - 1e-12:
            break
        take = min(q, (quote_amount - spent) / p)
        base += take
        spent += take * p
        fills.append((p, take))
    return base, spent, fills


@dataclass
class ExecConfig:
    latency_ms: float = 500.0
    leg_fail_prob: float = 0.02
    unwind_penalty: float = 0.001      # fracción del nocional al deshacer una pata
    seed: Optional[int] = None

    def statuses(self):
        return {"latency_ms": ASSUMED, "leg_fail_prob": ASSUMED, "unwind_penalty": ASSUMED}


class StrategyLedger:
    """Capital y P&L de UNA estrategia. Nunca se comparte entre estrategias."""

    def __init__(self, strategy, capital=100.0):
        self.strategy = strategy
        self.capital = capital
        self.cash = capital
        self.locked = 0.0
        self.peak_locked = 0.0
        self.realized = 0.0
        self.trades: List[dict] = []
        self.lock = threading.Lock()

    def can_commit(self, usd):
        return usd <= self.cash + 1e-9

    def commit(self, usd):
        with self.lock:
            if usd > self.cash + 1e-9:
                raise ValueError("capital insuficiente")
            self.cash -= usd
            self.locked += usd
            self.peak_locked = max(self.peak_locked, self.locked)

    def release(self, usd, pnl, trade: dict):
        with self.lock:
            self.locked -= usd
            self.cash += usd + pnl
            self.realized += pnl
            self.trades.append({**trade, "pnl": pnl, "capital": usd})

    def summary(self):
        return {"strategy": self.strategy, "capital": self.capital, "cash": self.cash,
                "locked": self.locked, "peak_locked": self.peak_locked,
                "realized": self.realized, "trades": len(self.trades),
                "return_on_capital": self.realized / self.capital}


COST_STRESS = 1.5
# Datos faltantes o sospechosos: no se puede verificar, haya o no neto estimado.
UNVERIFIABLE_REASONS = ("STALE", "SUSPICIOUS", "NO_BOOK", "MISSING", "NO_TRADES", "NO_QUOTES",
                        "ERROR", "NO_DATA", "UNAVAILABLE", "NO_MODEL")
# Hay datos y edge estimado, pero no se puede ejecutar con nuestro capital/libro.
NOT_EXECUTABLE_REASONS = ("MIN_SIZE", "BUDGET", "NO_CAPITAL", "INSUFFICIENT_DEPTH", "INFEASIBLE")


def classify_lab(o, nature):
    """Clasificación común (misma regla que src/guarantee.py).

    nature: "arbitrage" (puede ser garantizado), "statistical" (ventaja
    estimada por un modelo; nunca garantizada; alias histórico "speculative")
    o "unverifiable" (requiere verificación manual que no existe)."""
    from src.guarantee import (
        GUARANTEED, NO_EDGE, NOT_EXECUTABLE, STATISTICAL, UNVERIFIABLE,
    )
    sim = o.sim or {}
    net = sim.get("net_usd")
    filled = sim.get("status") == "FILLED"
    # Si la ejecución no se completó (desapareció, parcial, pata fallida), la
    # ventaja se juzga por el neto ESTIMADO: una oportunidad estimada positiva
    # que desaparece es NO_EJECUTABLE, no SIN_EDGE.
    positive = ((net if (net is not None and (filled or not sim)) else o.net_estimated_usd)
                > 0) if sim else (o.net_estimated_usd > 0 if net is None else net > 0)
    reason = o.reason or ""
    if nature in ("statistical", "speculative"):
        if any(k in reason for k in UNVERIFIABLE_REASONS):
            return UNVERIFIABLE, f"no verificable: {reason}"
        return (STATISTICAL, "ventaja estimada por modelo; depende de precios/funding "
                "futuros y exige validación fuera de muestra") if positive \
            else (NO_EDGE, "neto <= 0")
    if nature == "unverifiable":
        return UNVERIFIABLE, "requiere verificación manual que no existe"
    if any(k in reason for k in UNVERIFIABLE_REASONS):
        return UNVERIFIABLE, f"no verificable: {reason}"
    if not sim:
        if o.net_estimated_usd <= 0:
            return NO_EDGE, "neto estimado <= 0 después de costos"
        if any(k in reason for k in NOT_EXECUTABLE_REASONS):
            return NOT_EXECUTABLE, f"edge estimado pero no ejecutable: {reason}"
        return UNVERIFIABLE, f"neto estimado > 0 sin simulación de ejecución: {reason}"
    if sim.get("status") != "FILLED":
        return (NOT_EXECUTABLE, f"ejecución incompleta: {sim.get('status')}") if positive \
            else (NO_EDGE, f"ejecución {sim.get('status')} con neto <= 0")
    if net is None or net <= 0:
        return NO_EDGE, "ejecutada con neto <= 0"
    assumed = sum(c.usd for c in o.costs.values() if c.status == ASSUMED)
    if net - (COST_STRESS - 1) * assumed <= 0:
        return UNVERIFIABLE, f"no sobrevive a costos supuestos x{COST_STRESS}"
    return GUARANTEED, "ejecución completa simulada, neto > 0 con estrés de costos supuestos"


def make_rng(seed, strategy, tick):
    """RNG determinista por estrategia y tick (reproducible en replay)."""
    if seed is None:
        return random.Random()
    return random.Random(f"{seed}:{strategy}:{tick}")


def pct(x, d=3):
    return "n/d" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.{d}f}%"


assert PAPER_ONLY, "el laboratorio es solo simulación"
