"""Datos fijos y reproducibles para los tests del laboratorio."""

from lab.core import ExecConfig, LiquidityRegistry, StrategyLedger
from lab.modules.base import Context
from lab.sources import Snapshot

TS = "2026-10-09T12:00:00.000+00:00"
TS2 = "2026-10-09T12:00:00.300+00:00"


def book(bids, asks, ts=TS):
    return {"bids": [list(x) for x in bids], "asks": [list(x) for x in asks], "fetched_at": ts}


def snap(books, after=None, tick=0, markets=None, trades=None, polymarket=None, ts=TS):
    return Snapshot(tick=tick, ts=ts, books=books, books_after=after if after is not None else books,
                    markets=markets or {}, trades=trades or {}, polymarket=polymarket or {},
                    latency_ms=500)


def ctx(name, capital=100.0, seed=1, fail=0.0, registry=None, max_trade_fraction=0.5):
    return Context(exec_cfg=ExecConfig(seed=seed, leg_fail_prob=fail), registry=registry or LiquidityRegistry(),
                   ledger=StrategyLedger(name, capital), seed=seed,
                   max_trade_fraction=max_trade_fraction)
