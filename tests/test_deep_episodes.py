"""Episodios: persistencia contada una vez y verificación de ejecutabilidad."""

from lab import episodes


def opp(tick, net, status=None, key="k", strategy="s"):
    return {"strategy": strategy, "key": key, "tick": tick, "ts": f"2026-10-13T19:{tick:02d}:00+00:00",
            "stage": "SIMULATED" if status else "ESTIMATED", "net_estimated_usd": net,
            "reason": status or "ESTIMATED_POSITIVE", "sim": {"status": status, "net_usd": net} if status else None}


def test_consecutive_positive_ticks_form_one_episode():
    rows = [opp(0, 0.2, "FILLED"), opp(1, 0.2, "DISAPPEARED"), opp(2, 0.1), opp(5, 0.3)]
    eps = episodes.build(rows)
    assert [e["ticks"] for e in eps] == [3, 1]
    assert eps[0]["executable_at_verification"] == 1
    assert eps[0]["duration_s_min"] == 120
    assert set(eps[0]["reasons"]) == {"FILLED", "DISAPPEARED", "ESTIMATED_POSITIVE"}


def test_negative_estimates_never_create_episodes():
    assert episodes.build([opp(0, -0.1), opp(1, 0.0)]) == []


def test_duration_upper_bound_uses_next_tick_time():
    eps = episodes.build([opp(0, 0.2)], tick_ts={1: "2026-10-13T19:01:00+00:00"})
    assert eps[0]["duration_s_min"] == 0 and eps[0]["duration_s_max"] == 60
    s = episodes.summarize(eps)
    assert s["s"]["episodes"] == 1 and s["s"]["with_executable_tick"] == 0
