"""Monitor de cash-and-carry: esperado, observado y riesgo separados; regla congelada."""

import pytest

from lab import carry_monitor as cm


def meta(exp_ms):
    return {"binance|ETH/USDT:USDT-X": {"venue": "binance", "spot": "ETH/USDT", "expiry": exp_ms}}


def books(s, f):
    return {"binance|ETH/USDT": {"asks": [[s, 10]], "bids": [[s - 0.1, 10]]},
            "binance|ETH/USDT:USDT-X": {"bids": [[f, 10]], "asks": [[f + 0.1, 10]]}}


DAY = 86_400_000


def test_signal_only_when_locked_return_beats_tbill():
    rows = cm.evaluate(books(100.0, 100.87), meta(73 * DAY), 0, rate_pct=4.05)
    (r,) = rows
    assert r["signal"] == 0 and r["ex_ante_excess_1x_pct"] < 0          # el caso real de octubre
    (r,) = cm.evaluate(books(100.0, 104.0), meta(73 * DAY), 0, rate_pct=4.05)
    assert r["signal"] == 1
    assert r["observed_net_1x_pct"] is None                              # observado solo al vencer
    assert r["liq_price_1x"] == pytest.approx(2 * 104.0 / 1.005)


def test_save_settle_and_summary(tmp_path):
    p = tmp_path / "m.sqlite"
    rows = cm.evaluate(books(100.0, 104.0), meta(73 * DAY), 0, rate_pct=4.0)
    cm.save(rows, "2026-10-13T00:00:00+00:00", p)
    cm.save(rows, "2026-10-13T00:00:00+00:00", p)                       # sin duplicar
    s = cm.summary(p)
    assert s["observations"] == 1 and s["signals"] == 1 and s["settled"] == 0
    assert cm.settle({("binance", 73 * DAY): 130.0}, p) == 1
    assert cm.summary(p)["settled"] == 1
