"""C3: box spread con precios ejecutables (comprar al ask, vender al bid) y comisiones."""

from datetime import datetime, timezone

import pytest

from lab.research import deribit_parity as dp


def row(name, bid, ask):
    return {"instrument_name": name, "bid_price": bid, "ask_price": ask}


def test_box_cost_uses_executable_sides_and_fees():
    now = datetime(2026, 10, 16, 8, tzinfo=timezone.utc)
    s = [row("BTC-25DEC26-70000-C", 0.150, 0.152), row("BTC-25DEC26-80000-C", 0.090, 0.092),
         row("BTC-25DEC26-70000-P", 0.020, 0.022), row("BTC-25DEC26-80000-P", 0.080, 0.082)]
    b = dp.boxes(s, 80000.0, now, tbill_pct=4.0, max_capital=2000.0)
    assert len(b) == 1
    x = b[0]
    legs = [0.152, 0.090, 0.082, 0.020]
    cost = ((0.152 - 0.090 + 0.082 - 0.020) * 0.1 + sum(dp.fee_btc(p) for p in legs)) * 80000
    assert x["cost_usd"] == pytest.approx(cost) and x["payoff_usd"] == pytest.approx(1000.0)
    assert x["period_ret_pct"] == pytest.approx(((1000 - 2 * dp.DFEE * 0.1 * 80000) / cost - 1) * 100)
    assert x["sell_proceeds_usd"] < x["cost_usd"]                      # el spread separa las dos puntas


def test_box_over_capital_limit_is_skipped():
    now = datetime(2026, 10, 16, 8, tzinfo=timezone.utc)
    s = [row("BTC-25DEC26-40000-C", 0.50, 0.51), row("BTC-25DEC26-80000-C", 0.05, 0.06),
         row("BTC-25DEC26-40000-P", 0.001, 0.002), row("BTC-25DEC26-80000-P", 0.05, 0.06)]
    assert dp.boxes(s, 80000.0, now, 4.0, max_capital=1000.0) == []    # cuesta ~US$3.900
