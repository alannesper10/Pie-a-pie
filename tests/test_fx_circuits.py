"""Circuitos cambiarios: puntas ejecutables, costos de transferencia y datos sospechosos."""

import pytest

from lab.research import fx_circuits as fc


def test_wire_cost_follows_galicia_schedule():
    # > USD 1.000: 0,3% mín. USD 125 + 0,10% cuenta en USD, IVA 21% sobre comisiones, + USD 10 corresponsal
    assert fc.wire_cost(10_000) == pytest.approx((125 + 10) * 1.21 + 10)
    assert fc.wire_cost(50_000) == pytest.approx((150 + 50) * 1.21 + 10)


def test_mep_legs_use_executable_sides_and_reject_crossed_quotes():
    bd = {"AL30": (86270, 1000, 86290, 1000), "AL30D": (56.10, 500, 56.11, 500)}
    legs = fc.fx_legs(bd, "D")
    assert legs["AL30"]["buy"] == pytest.approx(86290 / 56.10)     # comprar USD: ARS ask / USD bid
    assert legs["AL30"]["sell"] == pytest.approx(86270 / 56.11)    # vender USD: ARS bid / USD ask
    snap = {"data912_bonds": {"data": [{"symbol": "AL30", "px_bid": 86300, "px_ask": 86290, "q_bid": 1, "q_ask": 1}]}}
    assert fc.bonds(snap) == {}                                      # punta cruzada: inválida


def test_criptoya_outliers_are_flagged_not_used():
    snap = {"i": 0, "ts": "t", "errors": [],
            "binance_usdtars": {"data": {"bids": [["1615", "100"]], "asks": [["1615.2", "100"]]}},
            "criptoya_usdt_ars": {"data": {"a": {"totalAsk": 1610, "totalBid": 1605},
                                           "mexcp2p": {"totalAsk": 1607, "totalBid": 1800}}}}
    r = fc.analyze(snap)
    assert r["cy_suspicious"] == ["mexcp2p"]
    assert r["cy_cross_gross"] == pytest.approx(1605 / 1607 - 1)      # 1800 descartado
