from src import compare
from src.paper_trader import PaperBook
from src.strategies.kalshi_common import (
    DISCARD_FIELDS, OPPORTUNITY_FIELDS, PAPER_FIELDS, STRATEGY_CYCLE_FIELDS,
)
from src.tracking import (
    CYCLE_FIELDS, DURATION_FIELDS, NEAR_MISS_FIELDS, append_csv, save_json,
)


def _seed_current(d):
    append_csv(d / "cycles.csv", CYCLE_FIELDS, {"timestamp": "t", "ok": 1})
    append_csv(d / "cycles.csv", CYCLE_FIELDS, {"timestamp": "t2", "ok": 0})
    append_csv(d / "near_misses.csv", NEAR_MISS_FIELDS, {
        "event_ticker": "A", "ask_sum": 0.99, "est_fees": 0.03, "est_net": -0.04,
        "depth_with_edge": 0, "executable": False, "reason": "NO_POSITIVE_MARGINAL_EDGE"})
    save_json(d / "state.json", {"paper": PaperBook(cash=100.0).to_dict(), "streaks": {}})


def _seed_strategy(root, name, cash, executable=False):
    d = root / name
    append_csv(d / "cycles.csv", STRATEGY_CYCLE_FIELDS, {"timestamp": "t", "strategy": name, "ok": 1})
    append_csv(d / "opportunities.csv", OPPORTUNITY_FIELDS, {
        "strategy": name, "event_ticker": "E", "net_profit": 0.3 if executable else -0.01,
        "max_contracts_available": 5 if executable else 0, "fees": 0.02,
        "executable": executable, "reason": "NET_EDGE_OK" if executable else "INSUFFICIENT_DEPTH",
        "detail": "min_bundle_outlay=0.98"})
    append_csv(d / "discards.csv", DISCARD_FIELDS,
               {"timestamp": "t", "strategy": name, "reason": "LOW_VOLUME", "count": 7})
    append_csv(d / "durations.csv", DURATION_FIELDS,
               {"event_ticker": "E", "cycles": 2, "minutes": 25, "end_reason": "EDGE_GONE"})
    if executable:
        append_csv(d / "paper_trades.csv", PAPER_FIELDS,
                   {"action": "OPEN", "fees": 0.1, "slippage": 0.01})
    save_json(d / "state.json", {"paper": PaperBook(cash=cash).to_dict(), "streaks": {}})


def test_each_strategy_keeps_its_own_capital_and_pnl(tmp_path):
    _seed_current(tmp_path)
    root = tmp_path / "strategies"
    _seed_strategy(root, "buy_all_no", 100.0)
    _seed_strategy(root, "strike_inconsistency", 93.5, executable=True)
    c = compare.build(tmp_path, tmp_path / "no_funding_reports")
    assert c["kalshi_current"]["cash"] == 100.0
    assert c["buy_all_no"]["cash"] == 100.0
    assert c["strike_inconsistency"]["cash"] == 93.5          # no se mezcla
    assert c["strike_inconsistency"]["executable"] == 1
    assert c["strike_inconsistency"]["net_positive"] == 1
    assert c["strike_inconsistency"]["paper_fees"] == 0.1
    assert c["buy_all_no"]["executable"] == 0 and c["buy_all_no"]["net_positive"] == 0
    assert c["buy_all_no"]["discard_reasons"] == {"LOW_VOLUME": 7}
    assert c["buy_all_no"]["duration_minutes"]["mean"] == 25


def test_zero_is_reported_as_zero(tmp_path):
    _seed_current(tmp_path)
    c = compare.build(tmp_path, tmp_path / "nada")
    k = c["kalshi_current"]
    assert (k["opportunities"], k["net_positive"], k["executable"]) == (1, 0, 0)
    assert k["cycles"] == 2 and k["cycles_ok"] == 1
    f = c["funding_basis"]
    assert f["opportunities"] == 0 and f["executable"] == 0 and f["cash"] == 100.0
    s = c["strike_inconsistency"]
    assert s["cycles"] == 0 and s["opportunities"] == 0       # sin datos todavía


def test_render_has_all_strategies_and_metrics(tmp_path):
    _seed_current(tmp_path)
    text = compare.render(compare.build(tmp_path, tmp_path / "nada"))
    for s in compare.STRATEGIES:
        assert s in text
    for label in ("Oportunidades", "Net-positive", "Ejecutables", "Descartadas",
                  "Capital bloqueado", "P&L realizado", "Tamaño disponible"):
        assert label in text


def test_funding_reads_phase0_and_live(tmp_path):
    _seed_current(tmp_path)
    rep = tmp_path / "rep"
    save_json(rep / "phase0_summary.json", {"totals": {
        "pairs_ok": 9, "decisions": 100, "ex_ante_positive": 0, "trades": 0,
        "net_positive_trades": 0, "executable_trades_100usd": 0,
        "feasible_pairs_100usd": 7, "net_usd_total_all_pairs": 0.0}, "pairs": []})
    save_json(rep / "live_summary.json", {"snapshots": 45, "opportunities": 0, "errors": 0,
                                          "paper": {"cash": 100.0, "locked": 0.0}})
    f = compare.build(tmp_path, rep)["funding_basis"]
    assert f["discarded"] == 100 and f["cycles"] == 45
    assert f["discard_reasons"]["INFEASIBLE_MIN_SIZE_100USD_PAIRS"] == 2
