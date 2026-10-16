"""P6: señal sin mirar el futuro, costos, exclusión de no binarios y agregación por evento."""

import pytest

from lab.research import longshot as ls

END = "2025-03-01T00:00:00Z"
T_END = 1740787200                      # 2025-03-01 00:00 UTC


def market(prices='["1", "0"]', fees=False):
    return {"id": "m1", "event_key": "e1", "outcomes": '["Yes", "No"]', "outcomePrices": prices,
            "clobTokenIds": '["A", "B"]', "endDate": END, "closedTime": "2025-03-02 00:00:00+00",
            "feesEnabled": fees, "feeSchedule": {"rate": 0.05}, "category_key": "x"}


def test_signal_uses_price_at_least_7_days_before_end():
    h = [{"t": T_END - 10 * 86400, "p": 0.90}, {"t": T_END - 3 * 86400, "p": 0.99}]
    assert ls.signal_price(h, ls.ts(END)) == 0.90          # el 0,99 de 3 días antes no se usa


def test_buys_favorite_in_band_with_costs_and_pays_on_win():
    hist = {"A": [{"t": T_END - 8 * 86400, "p": 0.90}], "B": [{"t": T_END - 8 * 86400, "p": 0.10}]}
    t = ls.trade(market(fees=True), hist)
    assert len(t) == 1 and t[0]["won"]
    cost = 0.90 + 0.005 + 0.05 * 0.90 * 0.10
    assert t[0]["ret_pct"] == pytest.approx((1 - cost) / cost * 100)
    lose = ls.trade(market(prices='["0", "1"]'), hist)
    assert lose[0]["ret_pct"] == pytest.approx(-100.0)


def test_void_or_non_binary_markets_are_excluded_and_events_averaged():
    hist = {"A": [{"t": T_END - 8 * 86400, "p": 0.90}]}
    assert ls.trade(market(prices='["0.5", "0.5"]'), hist) == []
    ev = ls.by_event([{"event": "e", "market": "m1", "ret_pct": 10, "days": 7, "closed": "2025-03-02", "category": "x"},
                      {"event": "e", "market": "m2", "ret_pct": -100, "days": 8, "closed": "2025-03-03", "category": "x"}])
    assert len(ev) == 1 and ev[0]["ret_pct"] == pytest.approx(-45)
