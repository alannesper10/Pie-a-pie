"""Basis/funding: spot largo + perp corto en el mismo exchange.

Reutiliza funding/ (LiveRunner, simulador paper, costos). En el laboratorio
usa su PROPIA base por corrida (no toca funding_data/ ni el ledger standalone)
y pasa los libros spot por el registro de liquidez compartida para que no se
use dos veces la misma liquidez que cross_exchange o triangular.
"""

import logging

from ..core import ACCEPTED, REJECTED, Cost, Opportunity
from .base import Module

log = logging.getLogger("lab.basis")


class RegistryBooks:
    """Fuente de libros para LiveRunner que descuenta la liquidez spot ya usada."""

    def __init__(self, adapters):
        self.adapters = adapters
        self.registry = None

    def get(self, exchange, asset, limit=50):
        b = self.adapters[exchange].fetch_books(asset, limit)
        if self.registry is not None:
            sym = f"{asset}/USDT"
            b["spot_asks"] = [list(x) for x in self.registry.available(
                exchange, sym, "asks", [tuple(x) for x in b["spot_asks"]])]
            b["spot_bids"] = [list(x) for x in self.registry.available(
                exchange, sym, "bids", [tuple(x) for x in b["spot_bids"]])]
        return b

    def close(self):
        pass


class BasisFunding(Module):
    name = "basis_funding"
    nature = "statistical"   # el funding futuro y el basis no están garantizados
    replayable = False      # usa datos de perpetuos en vivo propios

    def __init__(self, db_path, seed=None, exchanges=None, assets=None, runner=None):
        from funding.config import FundingConfig
        cfg = FundingConfig()
        if exchanges:
            cfg = FundingConfig(**{**cfg.__dict__, "exchanges": tuple(exchanges)})
        if assets:
            cfg = FundingConfig(**{**cfg.__dict__, "assets": tuple(assets)})
        self.cfg = cfg
        if runner is None:
            from funding.adapters import make_adapter
            from funding.live import LiveRunner
            from funding.storage import Storage
            adapters = {}
            for n in cfg.exchanges:
                try:
                    adapters[n] = make_adapter(n)
                except Exception as e:  # noqa: BLE001
                    log.error("adaptador %s: %s", n, e)
            self.books = RegistryBooks(adapters)
            runner = LiveRunner(cfg, adapters, Storage(db_path), self.books, log, seed=seed)
        else:
            self.books = runner.books
        self.runner = runner

    def evaluate(self, snap, ctx):
        self.books.registry = ctx.registry
        led = self.runner.state.ledger
        before_open = set(led.open)
        before_closed = len(led.closed)
        res = self.runner.tick()
        out = []
        for (ex, asset), s in res.items():
            key = f"{ex}|{asset}"
            o = Opportunity(strategy=self.name, key=key, tick=snap.tick, ts=snap.ts,
                            venues=[ex], instruments=[f"{asset}/USDT", f"{asset}/USDT:USDT"],
                            observed={}, assumptions=[
                                "funding esperado = mín(tasa actual, media de 3 períodos)",
                                "horizonte 7 días; basis esperado 0", "1x de apalancamiento"])
            if not s.get("ok"):
                o.reason = s.get("reason", "ERROR")
                out.append(o)
                continue
            n = s["notional"]
            o.observed = {k: s.get(k) for k in (
                "spot_bid", "spot_ask", "perp_bid", "perp_ask", "mark", "index_price",
                "funding_rate", "funding_interval_h", "next_funding_ts", "basis_pct",
                "trailing_rate", "liq_distance", "risks")}
            o.stage = "ESTIMATED"
            o.size, o.capital_usd = s["qty"], s["capital_required"]
            o.gross_usd = (s["expected_net_pct"] + s["cost_pct"] + s["leg_fail_cost_pct"]) * n
            o.costs = {name: Cost(c["value"] * n, c["status"], c["source"])
                       for name, c in s["costs"].items()}
            o.costs["falla_de_pata_esperada"] = Cost(s["leg_fail_cost_pct"] * n, "ASSUMED",
                                                     "prob. x costo de deshacer")
            k = led.key(ex, asset)
            if k in led.open and k not in before_open:
                pos = led.open[k]
                o.stage, o.decision, o.reason = "SIMULATED", ACCEPTED, "PAPER_OPENED"
                o.sim = {"status": "OPEN", "qty": pos.qty, "entry_fees": pos.entry_fees,
                         "unmatched_cost": pos.entry_unmatched_cost, "realized": False,
                         "net_usd": None, "net_kind": "POSICION_ABIERTA"}
                ctx.registry.claim(ex, f"{asset}/USDT", "asks", [(pos.spot_entry, pos.qty)])
            elif k in before_open:
                o.reason = "POSITION_ALREADY_OPEN"
            elif not s["feasible_100usd"]:
                o.reason = "INFEASIBLE_MIN_SIZE"
            else:
                o.reason = ("ESTIMATED_POSITIVE_NOT_OPENED" if s["expected_net_pct"] > 0
                            else "EXPECTED_NET_NEGATIVE")
            out.append(o)
        # posiciones cerradas en este tick: P&L realizado
        for p in led.closed[before_closed:]:
            out.append(Opportunity(
                strategy=self.name, key=f"{p.exchange}|{p.asset}|close", tick=snap.tick,
                ts=snap.ts, venues=[p.exchange], instruments=[p.asset], observed={},
                stage="SIMULATED", capital_usd=p.locked, decision=ACCEPTED,
                reason=p.close_reason,
                sim={"status": "CLOSED", "net_usd": p.realized_net, "realized": True,
                     "net_pct_capital": p.realized_net / p.locked if p.locked else 0}))
        return out

    def ledger_summary(self):
        led = self.runner.state.ledger
        return {"cash": led.cash, "locked": led.locked, "realized": led.realized_net,
                "open": len(led.open), "closed": len(led.closed),
                "failed_entries": led.failed_entries}

    def close(self):
        try:
            self.runner.storage.put("paper_ledger", self.runner.state.ledger.to_dict())
            self.runner.storage.close()
        except Exception:  # noqa: BLE001
            pass
