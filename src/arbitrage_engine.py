from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Opportunity:
    yes_ask: float
    no_ask: float
    pair_cost: float
    gross_profit_per_contract: float
    gross_return: float
    estimated_fees: float
    estimated_slippage: float
    net_profit_per_contract: float
    net_return: float
    executable: bool
    reason: str

def evaluate_binary_arbitrage(
    yes_ask: float,
    no_ask: float,
    *,
    fee_per_contract: float = 0.0,
    slippage_per_contract: float = 0.0,
    min_net_edge: float = 0.0,
) -> Optional[Opportunity]:
    """Evalúa comprar YES + NO cuando el payout conjunto es 1.00."""
    if not (0 < yes_ask < 1 and 0 < no_ask < 1):
        return None

    pair_cost = yes_ask + no_ask
    gross_profit = 1.0 - pair_cost
    gross_return = gross_profit / pair_cost if pair_cost else 0.0

    fees = max(0.0, fee_per_contract)
    slippage = max(0.0, slippage_per_contract)
    net_profit = gross_profit - fees - slippage
    net_return = net_profit / pair_cost if pair_cost else 0.0

    executable = net_profit > 1e-12 and net_return >= min_net_edge
    reason = "NET_EDGE_OK" if executable else "INSUFFICIENT_NET_EDGE"

    return Opportunity(
        yes_ask=yes_ask,
        no_ask=no_ask,
        pair_cost=pair_cost,
        gross_profit_per_contract=gross_profit,
        gross_return=gross_return,
        estimated_fees=fees,
        estimated_slippage=slippage,
        net_profit_per_contract=net_profit,
        net_return=net_return,
        executable=executable,
        reason=reason,
    )
