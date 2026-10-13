import sys

import pytest

from lab.history import HistoryCache
from lab.resources import ResourceGuard, process_rss_mb, safe_workers
from lab.store import LabStore
from tests.lab_fixtures import book, snap

H = 3_600_000


def test_history_cache_only_downloads_missing_ranges(tmp_path):
    calls = []

    def fetch(since, until):
        calls.append((since, until))
        return [(t, 1, 1, 1, float(t // H), 1) for t in range(since - since % H, until + 1, H)
                if t >= since]

    c = HistoryCache(tmp_path / "h.sqlite")
    c.ensure("binance", "BTC/USDT", "1h", 10 * H, 20 * H, fetch)
    assert len(calls) == 1
    c.ensure("binance", "BTC/USDT", "1h", 10 * H, 20 * H, fetch)     # ya está: no descarga
    assert len(calls) == 1
    c.ensure("binance", "BTC/USDT", "1h", 5 * H, 25 * H, fetch)      # solo los extremos
    assert calls[1:] == [(5 * H, 10 * H - 1), (20 * H + 1, 25 * H)]
    assert len(c.bars("binance", "BTC/USDT", "1h")) == 21
    assert c.closes("binance", "BTC/USDT", "1h")[12 * H] == 12.0


def test_history_fetch_errors_are_logged_not_invented(tmp_path):
    c = HistoryCache(tmp_path / "h.sqlite")

    def boom(since, until):
        raise ConnectionError("fuente caída")

    r = c.ensure("yahoo", "SPY", "1d", 0, 10 * H, boom)
    assert r["errors"] and c.bars("yahoo", "SPY", "1d") == []
    assert c.db.execute("SELECT COUNT(*) FROM fetch_log WHERE error IS NOT NULL").fetchone()[0] == 1


def test_resource_guard_stops_on_memory_and_time():
    g = ResourceGuard(max_rss_mb=100, rss_fn=lambda: 150.0)
    ok, why = g.check()
    assert not ok and "memoria" in why and g.peak_rss == 150
    t = iter([0.0, 5.0, 100.0])
    g = ResourceGuard(max_rss_mb=1e9, max_seconds=60, rss_fn=lambda: 10.0, clock=lambda: next(t))
    assert g.check()[0] is True
    assert g.check()[0] is False


@pytest.mark.skipif(sys.platform not in ("win32", "linux"), reason="lector de memoria por SO")
def test_regression_rss_reader_is_not_blind():
    # Bug: en Windows el handle de 64 bits se truncaba y devolvía None.
    assert (process_rss_mb() or 0) > 1


def test_safe_workers_keeps_a_core_free():
    assert 1 <= safe_workers(64) <= max(1, (__import__("os").cpu_count() or 2) - 1)


def test_snapshots_iterate_one_by_one_and_resume_tick(tmp_path):
    st = LabStore(tmp_path / "l.sqlite")
    for t in range(3):
        st.save_snapshot("r", snap({"binance|BTC/USDT": book([(1, 1)], [(2, 1)])}, tick=t))
    it = st.iter_snapshots("r")
    assert next(it).tick == 0                       # generador, no lista
    assert [s.tick for s in st.iter_snapshots("r", start_tick=1)] == [1, 2]
    assert st.max_tick("r") == 2 and st.max_tick("otra") == -1
