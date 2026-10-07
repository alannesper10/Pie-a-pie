from src.arbitrage_engine import evaluate_binary_arbitrage

def test_clean_arbitrage():
    opp = evaluate_binary_arbitrage(0.47, 0.49)
    assert opp is not None
    assert opp.pair_cost == 0.96
    assert round(opp.gross_profit_per_contract, 10) == 0.04
    assert opp.executable

def test_no_arbitrage():
    opp = evaluate_binary_arbitrage(0.51, 0.50)
    assert opp is not None
    assert not opp.executable
    assert opp.pair_cost == 1.01

def test_costs_can_kill_arbitrage():
    opp = evaluate_binary_arbitrage(
        0.49, 0.50,
        fee_per_contract=0.005,
        slippage_per_contract=0.005,
    )
    assert opp is not None
    assert not opp.executable

def test_minimum_edge():
    opp = evaluate_binary_arbitrage(
        0.47, 0.49,
        min_net_edge=0.05,
    )
    assert opp is not None
    assert not opp.executable
