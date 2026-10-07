"""Paper trading de spot largo + perp corto. Conservador y sin órdenes reales.

Supuestos explícitos:
  * Latencia: el que llama pasa los libros observados DESPUÉS de la latencia
    (en vivo se vuelve a pedir el libro), nunca los del momento de decidir.
  * Fills parciales: se barre la profundidad real; lo que no hay, no se llena.
  * Patas desparejas: si el perp llena menos que el spot, el exceso de spot se
    deshace vendiendo al bid con penalidad. Si la segunda pata falla (prob.
    configurable), se deshace toda la primera.
  * Rebalanceo: si la pérdida del perp supera un % del margen, se paga el costo
    de mover ese monto de spot a margen y se resetea la referencia (aprox.).
  * Liquidación: si el precio cruza el de liquidación se pierde el margen.
"""

import random
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

from .basis import basis_pnl
from .config import PAPER_ONLY, FundingConfig
from .costs import rebalance_cost_usd, walk_book
from .funding import funding_payment
from .risk import short_liquidation_price


@dataclass
class LegFill:
    qty: float
    avg: float
    notional: float
    fee: float


@dataclass
class EntryResult:
    status: str                 # FILLED | PARTIAL | LEG_FAILED_UNWOUND | NO_FILL
    qty: float                  # cantidad cubierta (igual en ambas patas)
    spot: Optional[LegFill]
    perp: Optional[LegFill]
    unmatched_qty: float = 0.0
    unmatched_cost: float = 0.0   # USD perdidos al deshacer la pata despareja
    fees: float = 0.0


def _fill(levels, qty, fee_rate):
    q, avg, notional = walk_book(levels, qty)
    return LegFill(q, avg, notional, notional * fee_rate)


def _unwind_spot(spot_bids, qty, entry_avg, cfg, exchange):
    """Vende `qty` de spot comprado a `entry_avg`: pérdida en USD (>= 0 si cae)."""
    fee = cfg.fee(exchange, "spot_taker").value
    q, avg, proceeds = walk_book(spot_bids, qty)
    if q < qty - 1e-12:   # ni siquiera hay bids: se asume salida al peor nivel
        worst = spot_bids[-1][0] if spot_bids else entry_avg * 0.98
        proceeds += (qty - q) * worst
    penalty = qty * entry_avg * cfg.unmatched_penalty.value
    return qty * entry_avg - proceeds + proceeds * fee + penalty


def simulate_entry(*, spot_asks, spot_bids, perp_bids, qty, cfg: FundingConfig,
                   exchange, rng: random.Random) -> EntryResult:
    """Compra spot y vende perp por `qty`, con libros observados tras la latencia."""
    assert PAPER_ONLY
    spot = _fill(spot_asks, qty, cfg.fee(exchange, "spot_taker").value)
    if spot.qty <= 0:
        return EntryResult("NO_FILL", 0.0, None, None)

    if rng.random() < cfg.leg_fail_prob.value:
        loss = _unwind_spot(spot_bids, spot.qty, spot.avg, cfg, exchange)
        return EntryResult("LEG_FAILED_UNWOUND", 0.0, spot, None,
                           unmatched_qty=spot.qty, unmatched_cost=loss + spot.fee,
                           fees=spot.fee)

    perp = _fill(perp_bids, spot.qty, cfg.fee(exchange, "perp_taker").value)
    unmatched = spot.qty - perp.qty
    unmatched_cost = 0.0
    if unmatched > 1e-12:
        unmatched_cost = _unwind_spot(spot_bids, unmatched, spot.avg, cfg, exchange)
    matched = perp.qty
    if matched <= 0:
        return EntryResult("LEG_FAILED_UNWOUND", 0.0, spot, perp, unmatched,
                           unmatched_cost + spot.fee, fees=spot.fee)
    # Se reporta la pata spot recortada a lo cubierto (el exceso ya se deshizo).
    kept = LegFill(matched, spot.avg, matched * spot.avg, spot.fee)
    status = "FILLED" if matched >= qty - 1e-12 else "PARTIAL"
    return EntryResult(status, matched, kept, perp, unmatched, unmatched_cost,
                       fees=spot.fee + perp.fee)


def simulate_exit(*, spot_bids, perp_asks, qty, cfg: FundingConfig, exchange):
    """Vende spot y recompra perp. Lo que falte de profundidad se cierra al peor
    nivel con penalidad (conservador). Devuelve (spot_avg, perp_avg, fees, extra)."""
    st, pt = cfg.fee(exchange, "spot_taker").value, cfg.fee(exchange, "perp_taker").value
    pen = cfg.unmatched_penalty.value

    def leg(levels, sign):
        q, avg, notional = walk_book(levels, qty)
        extra = 0.0
        if q < qty - 1e-12:
            worst = levels[-1][0] if levels else avg
            notional += (qty - q) * worst
            extra = (qty - q) * worst * pen
        return notional / qty, notional, extra

    s_avg, s_not, s_extra = leg(spot_bids, -1)
    p_avg, p_not, p_extra = leg(perp_asks, +1)
    return s_avg, p_avg, s_not * st + p_not * pt, s_extra + p_extra


@dataclass
class FundingPosition:
    exchange: str
    asset: str
    qty: float
    spot_entry: float
    perp_entry: float
    leverage: float
    opened_at: str
    entry_fees: float
    entry_unmatched_cost: float
    perp_ref: float = 0.0             # referencia para rebalanceo/liquidación
    funding_accrued: float = 0.0
    funding_events: int = 0
    rebalances: int = 0
    rebalance_costs: float = 0.0
    last_funding_ts: Optional[int] = None
    closed_at: Optional[str] = None
    close_reason: Optional[str] = None
    spot_exit: Optional[float] = None
    perp_exit: Optional[float] = None
    exit_fees: float = 0.0
    exit_extra: float = 0.0
    realized_net: Optional[float] = None

    @property
    def margin(self):
        return self.qty * self.perp_entry / self.leverage

    @property
    def locked(self):
        return self.qty * self.spot_entry + self.margin


@dataclass
class FundingPaperLedger:
    cash: float
    open: Dict[str, FundingPosition] = field(default_factory=dict)
    closed: List[FundingPosition] = field(default_factory=list)
    failed_entries: int = 0
    failed_entry_costs: float = 0.0

    @staticmethod
    def key(exchange, asset):
        return f"{exchange}:{asset}"

    @property
    def locked(self):
        return sum(p.locked for p in self.open.values())

    @property
    def realized_net(self):
        return sum(p.realized_net for p in self.closed) - self.failed_entry_costs

    def open_position(self, entry: EntryResult, *, exchange, asset, leverage, ts):
        """Registra la entrada. Bloquea spot + margen y descuenta costos."""
        if entry.status in ("NO_FILL", "LEG_FAILED_UNWOUND"):
            if entry.unmatched_cost:
                self.cash -= entry.unmatched_cost
                self.failed_entries += 1
                self.failed_entry_costs += entry.unmatched_cost
            return None
        pos = FundingPosition(
            exchange=exchange, asset=asset, qty=entry.qty,
            spot_entry=entry.spot.avg, perp_entry=entry.perp.avg, leverage=leverage,
            opened_at=ts, entry_fees=entry.fees,
            entry_unmatched_cost=entry.unmatched_cost, perp_ref=entry.perp.avg)
        outlay = pos.locked + pos.entry_fees + pos.entry_unmatched_cost
        if outlay > self.cash + 1e-9:
            raise ValueError("capital insuficiente para abrir la posición")
        self.cash -= outlay
        self.open[self.key(exchange, asset)] = pos
        return pos

    def accrue_funding(self, pos: FundingPosition, rate, mark, funding_ts):
        """Cobra/paga una liquidación de funding (una sola vez por timestamp)."""
        if pos.last_funding_ts is not None and funding_ts <= pos.last_funding_ts:
            return 0.0
        pay = funding_payment(rate, pos.qty, mark)
        pos.funding_accrued += pay
        pos.funding_events += 1
        pos.last_funding_ts = funding_ts
        return pay

    def check_risk(self, pos: FundingPosition, mark, cfg: FundingConfig):
        """Rebalanceo o liquidación según el precio del perp. Devuelve evento o None."""
        liq = short_liquidation_price(pos.perp_ref, pos.leverage,
                                      cfg.maintenance_margin.value)
        if mark >= liq:
            return "LIQUIDATION"
        loss = pos.qty * (mark - pos.perp_ref)
        if loss > cfg.rebalance_threshold.value * pos.margin:
            cost = rebalance_cost_usd(loss, cfg, pos.exchange)
            pos.rebalances += 1
            pos.rebalance_costs += cost
            self.cash -= cost
            pos.perp_ref = mark
            return "REBALANCE"
        return None

    def close_position(self, pos: FundingPosition, *, spot_exit, perp_exit,
                       exit_fees, exit_extra, ts, reason):
        price_pnl = basis_pnl(pos.qty, pos.spot_entry, pos.perp_entry,
                              spot_exit, perp_exit)
        if reason == "LIQUIDATION":
            # Se pierde el margen del perp; el spot se vende al precio de salida.
            price_pnl = pos.qty * (spot_exit - pos.spot_entry) - pos.margin
        proceeds = pos.locked + price_pnl + pos.funding_accrued - exit_fees - exit_extra
        self.cash += proceeds
        pos.spot_exit, pos.perp_exit = spot_exit, perp_exit
        pos.exit_fees, pos.exit_extra = exit_fees, exit_extra
        pos.closed_at, pos.close_reason = ts, reason
        pos.realized_net = (price_pnl + pos.funding_accrued - pos.entry_fees
                            - pos.entry_unmatched_cost - exit_fees - exit_extra
                            - pos.rebalance_costs)
        self.open.pop(self.key(pos.exchange, pos.asset), None)
        self.closed.append(pos)
        return pos.realized_net

    def to_dict(self):
        return {"cash": self.cash, "failed_entries": self.failed_entries,
                "failed_entry_costs": self.failed_entry_costs,
                "open": {k: asdict(p) for k, p in self.open.items()},
                "closed": [asdict(p) for p in self.closed]}

    @classmethod
    def from_dict(cls, d, starting_cash):
        if not d:
            return cls(cash=starting_cash)
        return cls(cash=d["cash"], failed_entries=d.get("failed_entries", 0),
                   failed_entry_costs=d.get("failed_entry_costs", 0.0),
                   open={k: FundingPosition(**p) for k, p in d.get("open", {}).items()},
                   closed=[FundingPosition(**p) for p in d.get("closed", [])])
