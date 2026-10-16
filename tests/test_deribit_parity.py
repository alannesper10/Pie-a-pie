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


def test_bound_violation_only_when_ask_below_intrinsic_after_fees():
    now = datetime(2026, 10, 16, 8, tzinfo=timezone.utc)
    rows = [{"instrument_name": "BTC-25DEC26-60000-C", "ask_price": 0.20, "underlying_price": 80000.0},   # intrínseco 0,25
            {"instrument_name": "BTC-25DEC26-60000-P", "ask_price": 0.01, "underlying_price": 80000.0},   # sin intrínseco
            {"instrument_name": "BTC-25DEC26-79000-C", "ask_price": 0.0124, "underlying_price": 80000.0}] # 0,0125 − costos < ask
    v = dp.bound_violations(rows, now)
    assert [x["instrument"] for x in v] == ["BTC-25DEC26-60000-C"]


def test_analyze_file_requires_two_consecutive_captures_for_persistence(tmp_path):
    import json as _j
    good = [row("BTC-25DEC26-70000-C", 0.150, 0.151), row("BTC-25DEC26-80000-C", 0.140, 0.141),
            row("BTC-25DEC26-70000-P", 0.010, 0.011), row("BTC-25DEC26-80000-P", 0.020, 0.021)]
    # box comprado a ~ (0,151−0,140+0,021−0,010)·0,1 = 0,0022 BTC ≈ US$176 por un pago de US$1.000: anómalo a propósito
    snaps = [{"ts": f"2026-10-16T18:0{i}:00+00:00", "index": 80000.0, "options": good} for i in range(3)]
    snaps.insert(1, {"ts": "2026-10-16T18:00:30+00:00", "error": "timeout"})
    p = tmp_path / "c3.jsonl"
    p.write_text("\n".join(_j.dumps(x) for x in snaps), encoding="utf-8")
    r = dp.analyze_file(p, lambda d: 4.0)
    assert r["snapshots"] == 4 and r["errors"] == 1 and len(r["rows"]) == 3
    assert ("B", "25DEC26", 70000, 80000) in r["persistent"]
