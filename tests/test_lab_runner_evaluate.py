import pytest

import lab.fees
from lab.core import ExecConfig, Opportunity
from lab.evaluate import build_report, out_of_sample, render_markdown, strategy_metrics, verdict
from lab.modules.base import Module
from lab.modules.cross_exchange import CrossExchange
from lab.modules.triangular import Triangular
from lab.runner import Lab
from lab.store import LabStore
from tests.lab_fixtures import TS, TS2, book, snap


class Boom(Module):
    name = "boom"

    def evaluate(self, s, c):
        raise RuntimeError("fuente caída")


def snaps(n=4):
    out = []
    for t in range(n):
        bid = 101.0 if t % 2 == 0 else 100.05
        b = {"binance|BTC/USDT": book([(99.9, 5)], [(100.0, 0.2)]),
             "okx|BTC/USDT": book([(bid, 0.2)], [(bid + 0.1, 5)], ts=TS2)}
        out.append(snap(b, tick=t, ts=f"2026-10-09T{10 + t:02d}:00:00.000+00:00"))
    return out


def run(tmp_path, name, seed=7, mods=None, fail=0.3):
    store = LabStore(tmp_path / "lab.sqlite")
    store.start_run(name, "2026-10-09T00:00:00", "replay", seed)
    lab = Lab(mods or [CrossExchange(symbols=("BTC/USDT",)), Triangular(), Boom()], store, name,
              ExecConfig(seed=seed, leg_fail_prob=fail))
    for s in snaps():
        lab.run_tick(s)
    lab.finish()
    return store


@pytest.fixture(autouse=True)
def no_rebalance(monkeypatch):
    monkeypatch.setitem(lab.fees.WITHDRAW_USD, "BTC", 0.0)


def test_module_error_is_isolated_and_logged(tmp_path):
    store = run(tmp_path, "r1")
    stats = {s: (n, errs) for s, n, _, errs in store.tick_stats("r1")}
    assert stats["boom"] == (4, 4)                      # falló en cada tick
    assert stats["cross_exchange"][1] == 0               # el resto siguió
    assert store.opportunities("r1", "cross_exchange")


def test_replay_with_same_seed_is_identical(tmp_path):
    a = run(tmp_path / "a", "x", seed=11)
    b = run(tmp_path / "b", "x", seed=11)
    strip = lambda rows: [(r["tick"], r["key"], r["reason"], (r.get("sim") or {}).get("net_usd"))  # noqa: E731
                          for r in rows]
    assert strip(a.opportunities("x")) == strip(b.opportunities("x"))
    assert a.ledgers("x") == b.ledgers("x")


def test_snapshot_roundtrip_for_replay(tmp_path):
    store = LabStore(tmp_path / "l.sqlite")
    s = snaps(1)[0]
    store.save_snapshot("r", s)
    (back,) = store.load_snapshots("r")
    assert back.books == s.books and back.tick == s.tick


def test_lab_never_writes_official_dataset(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run(tmp_path, "r2")
    assert not (tmp_path / "data").exists()


# --- evaluación --------------------------------------------------------------

def row(tick, net, cap=50.0, est_pct=0.002, hour=None, key="k", realized=True, costs=0.1,
        classification="ARBITRAJE_GARANTIZADO"):
    return {"tick": tick, "ts": f"2026-10-09T{hour if hour is not None else tick:02d}:00:00",
            "key": key, "decision": "ACCEPTED", "reason": "FILLED", "capital_usd": cap,
            "classification": classification,
            "gross_usd": net + costs, "net_estimated_usd": net, "net_estimated_pct": est_pct,
            "costs": {"fee": {"usd": costs}},
            "sim": {"net_usd": net, "net_pct_capital": net / cap, "realized": realized}}


def test_zero_is_zero_and_insufficient_evidence():
    m = strategy_metrics("s", [], None)
    assert m["evidence"]["simulated_executed"] == 0 and m["net_simulated_usd"] == 0
    assert m["verdict"]["label"] == "SIN EVIDENCIA SUFICIENTE"


def test_positive_but_few_trades_is_not_declared_profitable():
    m = strategy_metrics("s", [row(t, 0.5) for t in range(10)], None)
    assert m["net_simulated_usd"] > 0
    assert m["verdict"]["label"] == "SIN EVIDENCIA SUFICIENTE"


def test_profitable_requires_oos_stress_and_stable_periods():
    rows = [row(t, 0.3, hour=t % 12) for t in range(40)]
    m = strategy_metrics("s", rows, None)
    assert m["verdict"]["label"] == "RENTABLE (evidencia mínima)"
    # mismo neto pero los costos x1.5 lo dan vuelta -> NO RENTABLE
    rows = [row(t, 0.03, hour=t % 12, costs=0.1) for t in range(40)]
    assert strategy_metrics("s", rows, None)["verdict"]["label"] == "NO RENTABLE"


def test_not_realized_results_are_not_enough():
    rows = [row(t, 0.3, hour=t % 12, realized=False) for t in range(40)]
    assert strategy_metrics("s", rows, None)["verdict"]["label"] == "NO RENTABLE"


def test_out_of_sample_threshold_chosen_only_on_first_half():
    rows = ([row(t, 1.0, est_pct=0.001) for t in range(10)] +
            [row(t, -1.0, est_pct=0.001) for t in range(10, 20)])
    o = out_of_sample(rows)
    assert o["split_tick"] == 10 and o["in_sample_net"] > 0 and o["out_of_sample_net"] < 0


def test_report_renders_all_strategies(tmp_path):
    store = run(tmp_path, "r3")
    d = build_report(store, "r3")
    md = render_markdown(d)
    for n in ("cross_exchange", "triangular", "boom"):
        assert n in md
    assert "SIMULADO" in md and "Consolidado" in md
    assert d["consolidated"]["capital_total_usd"] == 300


def test_profit_that_is_not_guaranteed_does_not_count():
    rows = [row(t, 0.3, hour=t % 12, classification="NO_VERIFICABLE") for t in range(40)]
    m = strategy_metrics("cross_exchange", rows, None)
    assert m["evidence"]["simulated_executed"] == 0 and m["net_simulated_usd"] == 0
    assert m["classification"] == {"NO_VERIFICABLE": 40}
    assert m["verdict"]["label"] == "SIN EVIDENCIA SUFICIENTE"


def test_statistical_strategies_are_never_called_arbitrage():
    rows = [row(t, 0.3, hour=t % 12, classification="ESTADISTICA") for t in range(40)]
    m = strategy_metrics("liquidity_provision", rows, None)
    assert m["verdict"]["label"].startswith("ESTADISTICA:")
    assert m["verdict"]["label"].endswith("(no es arbitraje)")


def test_categories_are_never_mixed_in_totals():
    rows = ([row(t, 0.3, classification="ARBITRAJE_GARANTIZADO") for t in range(3)]
            + [row(t, 5.0, classification="NO_EJECUTABLE") for t in range(3)]
            + [row(t, -1.0, classification="SIN_EDGE") for t in range(3)])
    m = strategy_metrics("cross_exchange", rows, None)
    assert m["net_simulated_usd"] == pytest.approx(0.9)          # solo garantizadas
    cats = m["by_category"]
    assert cats["NO_EJECUTABLE"]["n"] == 3 and cats["SIN_EDGE"]["n"] == 3
    assert cats["ARBITRAJE_GARANTIZADO"]["net_simulated_usd"] == pytest.approx(0.9)


def test_sensitivity_separates_fees_and_slippage():
    r = row(0, 1.0, classification="ARBITRAJE_GARANTIZADO")
    r["costs"] = {"fee_compra": {"usd": 0.2}, "slippage_extra": {"usd": 0.1}}
    s = strategy_metrics("cross_exchange", [r], None)["sensitivity"]
    assert s["fees_x2"] == pytest.approx(0.8) and s["slippage_x2"] == pytest.approx(0.9)
    assert s["fees_x1.5_slippage_x2"] == pytest.approx(0.8)
