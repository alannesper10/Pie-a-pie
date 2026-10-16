"""P5: put spread con trades reales; lados ejecutables, riesgo definido y liquidación."""

from datetime import datetime, timezone

import pytest

from lab.research import options_putspread as op

E = datetime(2024, 2, 23, 8, tzinfo=timezone.utc)
ENTRY = datetime(2024, 1, 26, 8, tzinfo=timezone.utc)


def tr(k, price, direction, iv=60.0, S=40000.0):
    return {"instrument_name": f"BTC-{op.code(E)}-{k}-P", "price": price, "direction": direction,
            "iv": iv, "index_price": S}


def chain():
    return [tr(36000, 0.020, "sell"), tr(36000, 0.022, "buy"), tr(32000, 0.006, "buy"), tr(32000, 0.005, "sell"),
            tr(38000, 0.035, "sell"), tr(30000, 0.003, "buy"), tr(34000, 0.011, "buy")]


def test_picks_delta_strikes_and_executable_sides():
    t = op.build_trade(chain(), E, ENTRY, delivery_usd=45000.0)
    assert t["status"] == "OK"
    assert -0.32 < t["d1"] < -0.18 and t["k2"] < t["k1"]
    assert t["p1"] == pytest.approx(0.020 if t["k1"] == 36000 else t["p1"])   # lado "sell" (bid)
    assert t["pnl_usd"] == pytest.approx(t["prem_usd"])                        # vence fuera del dinero: se queda la prima
    assert t["max_loss_usd"] == pytest.approx((t["k1"] - t["k2"]) * 0.1 - t["prem_usd"])


def test_loss_is_capped_at_width_when_price_crashes():
    t = op.build_trade(chain(), E, ENTRY, delivery_usd=10000.0)
    assert t["pnl_usd"] < 0
    assert t["pnl_usd"] >= -t["max_loss_usd"] - 50          # tope + comisión de entrega


def test_missing_executable_side_is_not_verifiable():
    only_buys = [x for x in chain() if x["direction"] == "buy"]
    t = op.build_trade(only_buys, E, ENTRY, 45000.0)
    assert t["status"] == "NO_VERIFICABLE"
    assert op.build_trade([], E, ENTRY, 45000.0)["status"] == "NO_VERIFICABLE"
