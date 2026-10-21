"""Paper trading de paquetes intra-evento. No envía órdenes ni usa credenciales.

El costo (precio + comisiones + slippage estimado) sale de la caja al abrir y
queda bloqueado hasta que todas las patas del evento resuelven; recién ahí se
acredita el pago real según el resultado publicado por Kalshi.
"""

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


@dataclass
class PaperPosition:
    event_ticker: str
    legs: List[str]
    contracts: int
    cost: float
    fees: float
    slippage: float
    expected_net: float
    opened_at: str
    expected_close: Optional[str]
    closed_at: Optional[str] = None
    payout: Optional[float] = None
    # Lado comprado por pata ("yes"/"no"). None = todas YES (kalshi_current);
    # así el state.json existente se sigue cargando igual.
    sides: Optional[List[str]] = None
    # Entradas repetidas (solo estrategias que lo habilitan, p. ej. strike_inconsistency).
    # None en las posiciones existentes: se cargan y se guardan igual que antes.
    entry_id: Optional[str] = None          # identificador único de la entrada
    key: Optional[str] = None               # par/oportunidad al que pertenece
    entry_prices: Optional[List[float]] = None   # mejor ask por pata al entrar

    @property
    def outlay(self):
        return self.cost + self.fees + self.slippage

    @property
    def realized_net(self):
        return None if self.payout is None else self.payout - self.outlay


def leg_payout(market):
    """Pago por contrato YES de un mercado liquidado; None si aún no.

    Se espera a status=finalized: un resultado en determined/disputed/amended
    todavía puede cambiar. Un evento cancelado liquida cada pata como
    "scalar" a settlement_value_dollars (ej. KXOSCARVIS-27).
    """
    if market.get("status") != "finalized":
        return None
    result = (market.get("result") or "").lower()
    if result == "yes":
        return 1.0
    if result == "no":
        return 0.0
    if result == "scalar":
        try:
            return float(market.get("settlement_value_dollars"))
        except (TypeError, ValueError):
            return None
    return None


_OPTIONAL_FIELDS = ("sides", "entry_id", "key", "entry_prices")


def _pos_dict(pos):
    d = asdict(pos)
    for k in _OPTIONAL_FIELDS:
        if d.get(k) is None:
            d.pop(k, None)  # formato idéntico al de kalshi_current y de las posiciones previas
    return d


@dataclass
class PaperBook:
    cash: float
    open: List[PaperPosition] = field(default_factory=list)
    closed: List[PaperPosition] = field(default_factory=list)

    @property
    def locked(self):
        return sum(p.outlay for p in self.open)

    @property
    def realized_net(self):
        return sum(p.realized_net for p in self.closed)

    def has_open(self, event_ticker):
        return any(p.event_ticker == event_ticker for p in self.open)

    def has_entry(self, entry_id):
        return any(p.entry_id == entry_id for p in self.open + self.closed)

    def open_for_key(self, key, event_ticker=None):
        """Entradas abiertas de un par. Las posiciones previas sin `key` se
        asocian por event_ticker (p. ej. la de USCLIMATE abierta el 20/10)."""
        return [p for p in self.open
                if p.key == key or (p.key is None and event_ticker and p.event_ticker == event_ticker)]

    def reconcile(self, starting_cash):
        """Diferencia contable: caja + bloqueado − realizado − capital inicial.
        Debe ser 0: el mismo capital no puede estar en dos lugares."""
        return self.cash + self.locked - self.realized_net - starting_cash

    def try_open(self, opp, expected_close, now, *, allow_repeat=False, entry_id=None,
                 key=None, entry_prices=None):
        """Abre una posición paper. Devuelve (posición | None, motivo).

        Por defecto, una sola posición por evento (ALREADY_OPEN), como siempre.
        Con allow_repeat=True cada entrada es una posición independiente con su
        propio entry_id; la misma entry_id no se abre dos veces (DUPLICATE_ENTRY).
        """
        if not opp.executable or opp.contracts < 1:
            return None, "NOT_EXECUTABLE"
        if not allow_repeat:
            if self.has_open(opp.event_ticker):
                return None, "ALREADY_OPEN"
        else:
            if not entry_id:
                raise ValueError("allow_repeat requiere entry_id")
            if self.has_entry(entry_id):
                return None, "DUPLICATE_ENTRY"
        pos = PaperPosition(
            event_ticker=opp.event_ticker,
            legs=[t for t, _, _ in opp.legs],
            contracts=opp.contracts,
            cost=opp.pair_cost * opp.contracts,
            fees=opp.estimated_fees,
            slippage=opp.estimated_slippage,
            expected_net=opp.net_profit,
            opened_at=now,
            expected_close=expected_close,
            sides=(list(opp.sides) if getattr(opp, "sides", None) else None),
            entry_id=entry_id if allow_repeat else None,
            key=key if allow_repeat else None,
            entry_prices=entry_prices if allow_repeat else None,
        )
        if pos.outlay > self.cash:
            return None, "INSUFFICIENT_CASH"
        self.cash -= pos.outlay
        self.open.append(pos)
        return pos, "OPENED"

    def try_settle(self, pos, markets_by_ticker: Dict[str, dict], now):
        """Liquida si todas las patas resolvieron. Devuelve True si cerró."""
        per_contract = 0.0
        sides = pos.sides or ["yes"] * len(pos.legs)
        for ticker, side in zip(pos.legs, sides):
            m = markets_by_ticker.get(ticker)
            value = leg_payout(m) if m else None
            if value is None:
                return False
            per_contract += value if side == "yes" else 1.0 - value
        pos.payout = per_contract * pos.contracts
        pos.closed_at = now
        self.cash += pos.payout
        self.open.remove(pos)
        self.closed.append(pos)
        return True

    def to_dict(self):
        return {"cash": self.cash,
                "open": [_pos_dict(p) for p in self.open],
                "closed": [_pos_dict(p) for p in self.closed]}

    @classmethod
    def from_dict(cls, d, starting_cash):
        if not d:
            return cls(cash=starting_cash)
        return cls(cash=d["cash"],
                   open=[PaperPosition(**p) for p in d.get("open", [])],
                   closed=[PaperPosition(**p) for p in d.get("closed", [])])
