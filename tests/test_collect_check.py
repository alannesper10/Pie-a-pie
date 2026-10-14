"""Ventana horaria de la recolección de CCL, reanudación e integridad."""

import zlib
from datetime import datetime, timezone

import pytest

import run_lab
from lab import collect_check as cc
from lab.sources import Snapshot
from lab.store import LabStore


def utc(h, m, day=15):
    return datetime(2026, 10, day, h, m, tzinfo=timezone.utc)


def test_window_is_argentine_time():
    # 11:00-17:05 ART = 14:00-20:05 UTC
    assert cc.window_action(utc(13, 59), "11:00-17:05") == ("wait", 60.0)
    assert cc.window_action(utc(14, 0), "11:00-17:05") == ("run", 0.0)
    assert cc.window_action(utc(20, 4), "11:00-17:05") == ("run", 0.0)
    assert cc.window_action(utc(20, 5), "11:00-17:05") == ("stop", 0.0)
    # 01:00 UTC del 16 = 22:00 ART del 15: la ventana de ese día ya cerró
    assert cc.window_action(utc(1, 0, day=16), "11:00-17:05")[0] == "stop"
    with pytest.raises(ValueError):
        cc.parse_window("17:05-11:00")


def _store(tmp_path, ticks, ts=lambda t: f"2026-10-15T14:{t:02d}:00+00:00", errors=None):
    store = LabStore(tmp_path / "c.sqlite")
    store.start_run("r", "2026-10-15T14:00:00+00:00", "collect", 7, args={"sources": "ccl"})
    for t in ticks:
        s = Snapshot(tick=t, ts=ts(t), ccl={"byma": {"GGAL|2": {}}}, errors=(errors or {}).get(t, []))
        store.save_snapshot("r", s)
    return store


def test_verify_reports_missing_gaps_and_errors_without_filling(tmp_path):
    err = {"venue": "data912", "what": "arg_stocks", "error": "ReadTimeout"}
    store = _store(tmp_path, [0, 1, 2, 5, 6], errors={2: [err]})
    out = cc.verify_run(store.db, "r", interval_sec=60)
    assert out["missing_ticks"] == [3, 4] and out["ok"] is False
    assert out["time_gaps"] == [{"after_tick": 4, "tick": 5, "from": "2026-10-15T14:02:00+00:00",
                                 "to": "2026-10-15T14:05:00+00:00", "seconds": 180.0}]
    assert out["ticks_with_errors"] == {2: ["data912:arg_stocks"]}
    assert out["errors_by_source"] == {"data912:arg_stocks": 1}
    assert out["snapshots"] == 5                      # nada inventado para 3 y 4


def test_unreadable_last_snapshot_is_retaken_on_resume(tmp_path):
    store = _store(tmp_path, [0, 1, 2])
    store.db.execute("UPDATE snapshots SET data=? WHERE run_id='r' AND tick=2", (zlib.compress(b"{trunc"),))
    store.db.commit()
    assert cc.last_valid_tick(store.db, "r") == 1
    out = cc.verify_run(store.db, "r")
    assert out["unreadable_ticks"] == [2] and out["ok"] is False


def test_collect_waits_for_window_and_stops_at_close(tmp_path, monkeypatch):
    calls, sleeps = [], []
    # 13:58 espera; al despertar se relee el reloj (14:00) antes de capturar
    clock = iter([utc(13, 58), utc(14, 0), utc(14, 0), utc(14, 1), utc(20, 5)])

    class FakeDT(datetime):
        @classmethod
        def now(cls, tz=None):
            return next(clock)

    import datetime as dtmod
    monkeypatch.setattr(dtmod, "datetime", FakeDT)
    monkeypatch.setattr(run_lab, "DB", tmp_path / "w.sqlite")
    monkeypatch.setattr(run_lab.time, "sleep", lambda s: sleeps.append(s))

    def fake_snapshot(t, *a, **k):
        calls.append(k.get("ccl") is not None and k.get("futures") is None and a[0] is None and a[1] is None)
        return Snapshot(tick=t, ts=f"2026-10-15T14:0{t}:00+00:00", ccl={"byma": {"X|2": {}}})

    monkeypatch.setattr(run_lab, "build_snapshot", fake_snapshot)
    import lab.sources as srcmod
    monkeypatch.setattr(srcmod, "CclSource", lambda: object())
    run_lab.main(["collect", "--run", "w", "--sources", "ccl", "--ticks", "10",
                  "--interval-sec", "60", "--window-art", "11:00-17:05"])
    assert sleeps[0] == 60.0                          # esperó la apertura, de a 60 s
    assert calls == [True, True, True]                # solo CCL, 3 capturas y cierre
    store = LabStore(tmp_path / "w.sqlite")
    assert store.max_tick("w") == 2


def test_window_for_a_given_day_waits_overnight():
    from datetime import date
    act, wait = cc.window_action(utc(21, 0, day=14), "11:00-17:05", date(2026, 10, 15))
    assert act == "wait" and wait == 17 * 3600.0     # 18:00 ART del 14 -> 11:00 ART del 15
    assert cc.window_action(utc(21, 0, day=14), "11:00-17:05")[0] == "stop"
