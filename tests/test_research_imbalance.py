import pytest

from lab.research.imbalance import ImbalanceConfig, collect_series, evaluate, imbalance, trades_for
from tests.lab_fixtures import book, snap


def test_imbalance_top_levels():
    assert imbalance(book([(99, 3), (98, 1)], [(101, 1)])) == pytest.approx(0.6)


def test_trades_cross_the_spread_twice_and_pay_two_fees():
    ser = [(0, "t0", 0.9, 99.0, 101.0), (1, "t1", 0.0, 102.0, 103.0)]
    (t,) = trades_for(ser, 0.5, fee=0.001)
    assert t["gross"] == pytest.approx((102 - 101) / 101) and t["net"] == pytest.approx(t["gross"] - 0.002)
    assert trades_for([(0, "a", 0.9, 1, 2), (2, "b", 0, 3, 4)], 0.5, 0.0) == []   # no consecutivos


def test_series_from_snapshots_and_bh_over_all_hypotheses():
    snaps = []
    for t in range(60):
        imb_bid = 5 if t % 2 == 0 else 1
        mid = 100 + (0.5 if t % 2 else 0)          # sube después de desbalance comprador
        snaps.append(snap({"binance|BTC/USDT": book([(mid - 0.01, imb_bid)], [(mid + 0.01, 1)])},
                          tick=t))
    ser = collect_series(snaps)
    assert len(ser[("binance", "BTC/USDT")]) == 60
    free = evaluate(ser, ImbalanceConfig(fee=0.0, min_trades=5))
    assert free["hypotheses_tested"] == 3
    assert any(h["verdict"] == "ESTADISTICA" for h in free["results"])
    costly = evaluate(ser, ImbalanceConfig(fee=0.01, min_trades=5))
    assert all(h["verdict"] != "ESTADISTICA" for h in costly["results"])
