"""C1/C2: strangle comprado y volatilidad condicional con lados ejecutables."""

from datetime import datetime, timezone

import pytest

from lab.research import options_hull as oh
from lab.research.options_putspread import code

E = datetime(2024, 2, 23, 8, tzinfo=timezone.utc)
ENTRY = datetime(2024, 1, 26, 8, tzinfo=timezone.utc)
C = code(E)


def tr(k, cp, price, direction, iv=60.0, S=40000.0):
    return {"instrument_name": f"BTC-{C}-{k}-{cp}", "price": price, "direction": direction, "iv": iv, "index_price": S}


def book():
    rows = []
    for k, cp, p in [(40000, "C", 0.07), (40000, "P", 0.07), (52000, "C", 0.008), (30000, "P", 0.006),
                     (46000, "C", 0.02), (35000, "P", 0.02), (60000, "C", 0.002), (26000, "P", 0.002)]:
        rows += [tr(k, cp, p, "buy"), tr(k, cp, p * 0.95, "sell")]
    return rows


def test_strangle_buys_far_wings_at_ask_and_pays_on_crash():
    t = oh.strangle(book(), C, ENTRY, E, S_T=20000.0)
    assert t["status"] == "OK" and t["kp"] < 40000 < t["kc"]
    assert abs(t["dp"]) < 0.12 and t["dc"] < 0.12
    assert t["payoff"] == pytest.approx((t["kp"] - 20000) * 0.1)
    assert t["pnl"] > 0
    flat = oh.strangle(book(), C, ENTRY, E, S_T=40000.0)
    assert flat["pnl"] == pytest.approx(-flat["capital"])              # vence sin valor: pierde la prima


def test_conditional_vol_signals_and_defined_risk():
    long = oh.conditional_vol(book(), C, ENTRY, E, S_T=48000.0, sigma_fc=0.80)   # 0,80 > 1,1·0,60
    assert long["signal"] == "LONG_STRADDLE"
    assert long["pnl"] == pytest.approx(8000 * 0.1 - long["capital"] - 0.00015 * 0.1 * 48000)   # entrega
    short = oh.conditional_vol(book(), C, ENTRY, E, S_T=40000.0, sigma_fc=0.40)  # 0,40 < 0,9·0,60
    assert short["signal"] == "SHORT_IRON_FLY" and short["pnl"] > 0
    crash = oh.conditional_vol(book(), C, ENTRY, E, S_T=10000.0, sigma_fc=0.40)
    assert crash["pnl"] >= -crash["capital"] - 50                        # pérdida acotada (+ entrega)
    assert oh.conditional_vol(book(), C, ENTRY, E, S_T=40000.0, sigma_fc=0.60)["status"] == "SIN_SENAL"


def test_ewma_uses_fixed_lambda_and_needs_history():
    assert oh.ewma_vol([100.0] * 20) is None
    closes = [100 * (1.01 if i % 2 else 0.99) ** 0 * (1.01 ** (i % 2)) for i in range(60)]
    v = oh.ewma_vol(closes)
    assert v == pytest.approx(0.01 * (365 ** 0.5), rel=0.05)
