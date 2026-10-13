"""Registro económico común (EconomicRecord) para todas las estrategias y el
ejecutor de órdenes de HORUS.

Regla central: lo TEÓRICO (estimado/simulado, no realizado) y lo REALIZADO
nunca comparten campo. `realized_pnl_usd` solo se completa con una
liquidación o un cierre efectivo (en paper: el cierre simulado de una
posición, marcado como tal en `evidence`).
"""

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

EVIDENCE_LEVELS = ("OBSERVED", "ESTIMATED", "SIMULATED", "REALIZED_PAPER")


@dataclass
class EconomicRecord:
    source: str                       # "lab" | "kalshi" | "funding" | "executor"
    strategy: str
    key: str
    ts: str
    nature: str                       # arbitrage | statistical | unverifiable | horus_order
    evidence: str                     # uno de EVIDENCE_LEVELS
    category: str = ""                # ARBITRAJE_GARANTIZADO, ESTADISTICA, ...
    decision_reason: str = ""         # motivo de aceptación, rechazo o no verificación
    venues: List[str] = field(default_factory=list)
    instruments: List[str] = field(default_factory=list)
    capital_committed_usd: float = 0.0
    capital_locked_usd: float = 0.0
    lock_hours: Optional[float] = None
    observed_prices: dict = field(default_factory=dict)
    executed_prices: dict = field(default_factory=dict)
    gross_usd: float = 0.0
    costs_verified_usd: float = 0.0
    costs_assumed_usd: float = 0.0
    expected_net_usd: Optional[float] = None      # TEÓRICO (estimado o simulado)
    realized_pnl_usd: Optional[float] = None      # solo con cierre/liquidación
    unrealized_pnl_usd: Optional[float] = None    # posición abierta marcada a mercado
    slippage_bps: Optional[float] = None
    fill_ratio: Optional[float] = None            # ejecutado / pedido
    max_loss_usd: Optional[float] = None
    exposure_usd: Optional[float] = None
    data_sources: List[str] = field(default_factory=list)
    data_quality: str = ""                        # OK | STALE | THIRD_PARTY | DELAYED | INCOMPLETE
    out_of_sample: Optional[bool] = None
    extra: Dict = field(default_factory=dict)

    @property
    def costs_usd(self):
        return self.costs_verified_usd + self.costs_assumed_usd

    @property
    def expected_net_pct(self):
        if self.expected_net_usd is None or not self.capital_committed_usd:
            return None
        return self.expected_net_usd / self.capital_committed_usd

    @property
    def realized_pct(self):
        if self.realized_pnl_usd is None or not self.capital_committed_usd:
            return None
        return self.realized_pnl_usd / self.capital_committed_usd

    def validate(self):
        errs = []
        if self.evidence not in EVIDENCE_LEVELS:
            errs.append(f"evidencia desconocida: {self.evidence}")
        if self.realized_pnl_usd is not None and self.evidence != "REALIZED_PAPER":
            errs.append("resultado realizado sin evidencia de cierre (mezcla teórico y realizado)")
        if self.evidence == "REALIZED_PAPER" and self.realized_pnl_usd is None:
            errs.append("evidencia REALIZED_PAPER sin resultado realizado")
        if self.capital_locked_usd > self.capital_committed_usd + 1e-9:
            errs.append("capital bloqueado mayor que el comprometido")
        if self.fill_ratio is not None and not 0 <= self.fill_ratio <= 1 + 1e-9:
            errs.append("fill_ratio fuera de [0, 1]")
        return errs

    def to_dict(self):
        d = asdict(self)
        d.update(costs_usd=self.costs_usd, expected_net_pct=self.expected_net_pct,
                 realized_pct=self.realized_pct)
        return d


def from_lab_row(row: dict, nature: str = "arbitrage") -> EconomicRecord:
    """Opportunity.to_row() del laboratorio -> EconomicRecord. Una oportunidad
    del laboratorio NUNCA es realizada: a lo sumo SIMULATED."""
    sim = row.get("sim") or {}
    stage = row.get("stage") or "OBSERVED"
    evidence = stage if stage in EVIDENCE_LEVELS else "OBSERVED"
    expected = sim.get("net_usd") if sim.get("net_usd") is not None else (
        row.get("net_estimated_usd") if stage != "OBSERVED" else None)
    size = row.get("size") or 0
    matched = sim.get("matched")
    locked = (row.get("capital_usd") or 0) if sim.get("status") in ("FILLED", "PARTIAL") else 0.0
    return EconomicRecord(
        source="lab", strategy=row["strategy"], key=row["key"], ts=row["ts"], nature=nature,
        evidence=evidence, category=row.get("classification") or "",
        decision_reason=row.get("reason") or "", venues=list(row.get("venues") or []),
        instruments=list(row.get("instruments") or []),
        capital_committed_usd=row.get("capital_usd") or 0.0, capital_locked_usd=locked,
        lock_hours=row.get("lock_hours"), observed_prices=row.get("observed") or {},
        gross_usd=row.get("gross_usd") or 0.0,
        costs_verified_usd=row.get("costs_verified_usd") or 0.0,
        costs_assumed_usd=row.get("costs_assumed_usd") or 0.0,
        expected_net_usd=expected, realized_pnl_usd=None, unrealized_pnl_usd=None,
        fill_ratio=(matched / size) if (matched is not None and size) else None,
        max_loss_usd=row.get("max_loss_usd"),
        data_sources=list(row.get("venues") or []),
        extra={"sim_status": sim.get("status"), "assumptions": row.get("assumptions") or []})


def from_kalshi_position(pos: dict, ts: str, strategy="kalshi_current", category="") -> EconomicRecord:
    """Posición paper de Kalshi (data/state.json, SOLO LECTURA). Desembolso =
    cost + fees + slippage (src/paper_trader). Abierta: sin resultado
    realizado; cerrada (payout conocido): realizado = payout - desembolso."""
    outlay = float(pos.get("cost") or 0) + float(pos.get("fees") or 0) + float(pos.get("slippage") or 0)
    closed = pos.get("payout") is not None
    return EconomicRecord(
        source="kalshi", strategy=strategy, key=pos.get("event_ticker", ""), ts=ts,
        nature="arbitrage", evidence="REALIZED_PAPER" if closed else "SIMULATED",
        category=category, venues=["kalshi"], instruments=list(pos.get("legs") or []),
        capital_committed_usd=outlay, capital_locked_usd=0.0 if closed else outlay,
        lock_hours=None, expected_net_usd=pos.get("expected_net"),
        realized_pnl_usd=(float(pos["payout"]) - outlay) if closed else None,
        costs_assumed_usd=float(pos.get("fees") or 0) + float(pos.get("slippage") or 0),
        data_sources=["kalshi_public_api"], data_quality="OK",
        extra={"contracts": pos.get("contracts"), "opened_at": pos.get("opened_at"),
               "expected_close": pos.get("expected_close")})


def summarize(records: List[EconomicRecord]) -> dict:
    """Totales por estrategia; teórico y realizado en columnas separadas."""
    out = {}
    for r in records:
        d = out.setdefault(r.strategy, {"records": 0, "realized_count": 0, "realized_pnl_usd": 0.0,
                                        "expected_net_usd_open": 0.0, "capital_locked_usd": 0.0,
                                        "categories": {}})
        d["records"] += 1
        d["categories"][r.category or "SIN_CATEGORIA"] = d["categories"].get(r.category or "SIN_CATEGORIA", 0) + 1
        if r.realized_pnl_usd is not None:
            d["realized_count"] += 1
            d["realized_pnl_usd"] += r.realized_pnl_usd
        elif r.expected_net_usd is not None and r.capital_locked_usd > 0:
            d["expected_net_usd_open"] += r.expected_net_usd
        d["capital_locked_usd"] += r.capital_locked_usd
    return out
