"""Libro contable central del capital virtual (US$1.000 por defecto).

Un único fondo común. Cada estrategia tiene una cuenta con capital ASIGNADO;
dentro de él, el capital COMPROMETIDO en operaciones abiertas no se puede
reasignar ni volver a usar hasta liberarse. Invariantes (se verifican en
cada evento):
  sum(asignado) <= patrimonio total         (el mismo dólar no está en dos estrategias)
  0 <= comprometido <= asignado             (por estrategia)

Todo cambio es un EVENTO que se agrega a un registro JSONL (auditable). El
estado se reconstruye reproduciendo los eventos: nada se edita en el lugar.
Solo contabilidad virtual: no envía órdenes ni toca el ledger de Kalshi.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Account:
    strategy: str
    allocated: float = 0.0
    committed: float = 0.0
    realized: float = 0.0          # P&L realizado NETO de costos
    costs: float = 0.0
    gross: float = 0.0             # P&L realizado antes de costos
    unrealized: float = 0.0
    trades: List[dict] = field(default_factory=list)
    equity_curve: List[float] = field(default_factory=list)
    status: str = "INVESTIGACION"  # INVESTIGACION | VALIDACION | ACTIVA | SUSPENDIDA
    evidence: str = ""

    @property
    def available(self):
        return self.allocated - self.committed


class LedgerError(ValueError):
    pass


class CentralLedger:
    def __init__(self, initial_capital=1000.0, log_path: Optional[Path] = None):
        self.initial = initial_capital
        self.accounts: Dict[str, Account] = {}
        self.open: Dict[str, dict] = {}
        self.realized_total = 0.0
        self.log_path = Path(log_path) if log_path else None
        self.events: List[dict] = []
        self._replaying = False

    # ---- estado ----
    @property
    def equity(self):
        return self.initial + self.realized_total

    @property
    def unallocated(self):
        return self.equity - sum(a.allocated for a in self.accounts.values())

    def _acct(self, s):
        if s not in self.accounts:
            raise LedgerError(f"estrategia desconocida: {s}")
        return self.accounts[s]

    def _check(self):
        eps = 1e-9
        if sum(a.allocated for a in self.accounts.values()) > self.equity + eps:
            raise LedgerError("capital asignado mayor que el patrimonio")
        for a in self.accounts.values():
            if a.committed < -eps or a.committed > a.allocated + eps:
                raise LedgerError(f"{a.strategy}: comprometido fuera de [0, asignado]")

    def _event(self, kind, **data):
        ev = {"seq": len(self.events), "kind": kind, **data}
        self.events.append(ev)
        if self.log_path and not self._replaying:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    # ---- operaciones ----
    def register(self, strategy, evidence=""):
        if strategy in self.accounts:
            raise LedgerError(f"ya existe: {strategy}")
        self.accounts[strategy] = Account(strategy, evidence=evidence)
        self._event("register", strategy=strategy, evidence=evidence)

    def allocate(self, strategy, usd, reason=""):
        a = self._acct(strategy)
        if usd <= 0 or usd > self.unallocated + 1e-9:
            raise LedgerError(f"no hay {usd:.2f} sin asignar (libre {self.unallocated:.2f})")
        a.allocated += usd
        self._check()
        self._event("allocate", strategy=strategy, usd=usd, reason=reason)

    def deallocate(self, strategy, usd, reason=""):
        a = self._acct(strategy)
        if usd <= 0 or usd > a.available + 1e-9:
            raise LedgerError(f"{strategy}: solo {a.available:.2f} disponible (lo comprometido no se reasigna)")
        a.allocated -= usd
        self._check()
        self._event("deallocate", strategy=strategy, usd=usd, reason=reason)

    def commit(self, strategy, trade_id, usd, ts, detail=None):
        a = self._acct(strategy)
        if trade_id in self.open:
            raise LedgerError(f"operación repetida: {trade_id}")
        if usd <= 0 or usd > a.available + 1e-9:
            raise LedgerError(f"{strategy}: capital disponible {a.available:.2f} < {usd:.2f}")
        a.committed += usd
        self.open[trade_id] = {"strategy": strategy, "usd": usd, "ts": ts, "detail": detail or {}}
        self._check()
        self._event("commit", strategy=strategy, trade_id=trade_id, usd=usd, ts=ts, detail=detail or {})

    def mark(self, strategy, unrealized, ts):
        self._acct(strategy).unrealized = unrealized
        self._event("mark", strategy=strategy, unrealized=unrealized, ts=ts)

    def release(self, trade_id, gross_pnl, costs: Dict[str, float], ts):
        """Cierra una operación: P&L neto = bruto − costos. La ganancia o la
        pérdida queda en la cuenta de la estrategia (asignado += neto)."""
        if trade_id not in self.open:
            raise LedgerError(f"operación no abierta: {trade_id}")
        o = self.open.pop(trade_id)
        a = self.accounts[o["strategy"]]
        cost = sum(costs.values())
        net = gross_pnl - cost
        a.committed -= o["usd"]
        a.allocated += net
        a.realized += net
        a.gross += gross_pnl
        a.costs += cost
        self.realized_total += net
        a.trades.append({"trade_id": trade_id, "usd": o["usd"], "open_ts": o["ts"], "close_ts": ts,
                         "gross": gross_pnl, "costs": costs, "net": net, "net_pct": net / o["usd"] * 100})
        a.equity_curve.append(a.allocated)
        self._check()
        self._event("release", trade_id=trade_id, gross_pnl=gross_pnl, costs=costs, ts=ts)

    def set_status(self, strategy, status, evidence=""):
        a = self._acct(strategy)
        a.status, a.evidence = status, evidence or a.evidence
        self._event("status", strategy=strategy, status=status, evidence=evidence)

    # ---- reproducción ----
    @classmethod
    def replay(cls, log_path, initial_capital=1000.0):
        led = cls(initial_capital, log_path)
        led._replaying = True
        for line in open(log_path, encoding="utf-8"):
            ev = json.loads(line)
            k = ev.pop("kind")
            ev.pop("seq")
            if k == "register":
                led.register(ev["strategy"], ev.get("evidence", ""))
            elif k == "allocate":
                led.allocate(ev["strategy"], ev["usd"], ev.get("reason", ""))
            elif k == "deallocate":
                led.deallocate(ev["strategy"], ev["usd"], ev.get("reason", ""))
            elif k == "commit":
                led.commit(ev["strategy"], ev["trade_id"], ev["usd"], ev["ts"], ev.get("detail"))
            elif k == "mark":
                led.mark(ev["strategy"], ev["unrealized"], ev["ts"])
            elif k == "release":
                led.release(ev["trade_id"], ev["gross_pnl"], ev["costs"], ev["ts"])
            elif k == "status":
                led.set_status(ev["strategy"], ev["status"], ev.get("evidence", ""))
        led._replaying = False
        return led

    # ---- métricas ----
    def report(self):
        out = {"initial_capital": self.initial, "equity": self.equity,
               "net_return_pct": (self.equity / self.initial - 1) * 100,
               "unrealized_total": sum(a.unrealized for a in self.accounts.values()),
               "unallocated": self.unallocated, "strategies": {}}
        for s, a in self.accounts.items():
            nets = [t["net"] for t in a.trades]
            wins, losses = [x for x in nets if x > 0], [x for x in nets if x <= 0]
            peak, mdd, start = None, 0.0, a.allocated - a.realized
            for e in [start] + a.equity_curve:
                peak = e if peak is None else max(peak, e)
                if peak > 0:
                    mdd = min(mdd, e / peak - 1)
            used = sum(t["usd"] for t in a.trades)
            out["strategies"][s] = {
                "status": a.status, "evidence": a.evidence,
                "allocated": a.allocated, "committed": a.committed, "available": a.available,
                "realized_net": a.realized, "unrealized": a.unrealized, "gross": a.gross, "costs": a.costs,
                "costs_share_of_gross": a.costs / a.gross if a.gross > 0 else None,
                "trades": len(nets), "win_rate": len(wins) / len(nets) if nets else None,
                "avg_win": sum(wins) / len(wins) if wins else None,
                "avg_loss": sum(losses) / len(losses) if losses else None,
                "expectancy": sum(nets) / len(nets) if nets else None,
                "return_on_allocated_pct": a.realized / start * 100 if start > 0 else None,
                "return_on_used_pct": a.realized / used * 100 if used else None,
                "max_drawdown_pct": mdd * 100}
        return out
