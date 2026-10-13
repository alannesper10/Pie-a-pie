from dataclasses import dataclass
from typing import Optional

from ..core import ExecConfig, LiquidityRegistry, StrategyLedger


@dataclass
class Context:
    exec_cfg: ExecConfig
    registry: LiquidityRegistry
    ledger: StrategyLedger
    seed: Optional[int]
    max_trade_fraction: float = 0.5     # tope de capital por operación


class Module:
    name = "base"
    nature = "arbitrage"      # "arbitrage" | "speculative" | "unverifiable"
    needs_crypto_books = False
    needs_trades = False
    needs_polymarket = False

    def evaluate(self, snap, ctx):
        return []

    def execute(self, opp, snap, ctx):
        return None

    def close(self):
        pass
