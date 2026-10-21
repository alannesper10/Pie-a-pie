"""Rentabilidad mínima por plazo de recupero, casos A/B/C/D y autorizaciones (paper)."""

from datetime import datetime, timedelta, timezone
import json
from dataclasses import asdict

import pytest

from src.notify import _strategy_daily_lines, build_strategy_cycle_lines, compose_cycle_message
from src.paper_trader import PaperBook, PaperPosition
from src.strategies import entry_gate as eg
from src.strategies.kalshi_common import (
    OPPORTUNITY_FIELDS, BundleResult, StrategyStore, open_paper, open_paper_repeat, opportunity_row,
)
from src.tracking import read_csv

KEY = "USCLIMATE-2025|USCLIMATE-2030"
T0 = datetime(2026, 10, 21, 12, tzinfo=timezone.utc)


def ts(i):
    return (T0 + timedelta(minutes=40 * i)).isoformat(timespec="seconds")


def bundle(contracts=8, avail=20.0, prices=(0.129, 0.839), ret=0.15, fees=0.15, slip=0.016):
    """Paquete con neto esperado = ret × capital comprometido (costo + comisiones + slippage)."""
    outlay_per = 1.0 / (1 + ret)
    net_per = 1.0 - outlay_per
    cost = outlay_per * contracts - fees - slip
    return BundleResult(
        strategy="strike_inconsistency", event_ticker="USCLIMATE", key=KEY,
        legs=(("USCLIMATE-2025", prices[0], avail), ("USCLIMATE-2030", prices[1], avail)),
        sides=("yes", "no"), min_payout_per_bundle=1.0, contracts=contracts,
        max_contracts_available=avail, pair_cost=cost / contracts, cost=cost, min_payout=float(contracts),
        gross_profit=contracts - cost, estimated_fees=fees, estimated_slippage=slip,
        net_profit=net_per * contracts, net_profit_per_contract=net_per, net_return=net_per * contracts / cost,
        best_bundle_cost=cost / contracts, executable=True, reason="NET_EDGE_OK")


def legs_until(when, timer=0, status="active"):
    return [{"ticker": t, "status": status, "latest_expiration_time": when,
             "settlement_timer_seconds": timer} for t in ("USCLIMATE-2025", "USCLIMATE-2030")]


def legs_in(days, i=0):
    return legs_until((T0 + timedelta(minutes=40 * i) + timedelta(days=days)).isoformat())


def store(tmp_path, cash=100.0, open_=None):
    s = StrategyStore(tmp_path, "strike_inconsistency", 100.0, max_gap_min=40)
    s.book = PaperBook(cash=cash, open=list(open_ or []))
    return s


def go(s, r, i, markets, approvals=None, limit=25.0):
    return open_paper_repeat(s, r, "2030-12-31T15:00:00Z", ts(i), starting_cash=100.0,
                             max_key_outlay=limit, reference_rate=0.04, markets=markets,
                             approvals=approvals)


def decisions(tmp_path):
    return read_csv(tmp_path / "strike_inconsistency" / "decisions.csv")


def requests(tmp_path):
    return read_csv(tmp_path / "strike_inconsistency" / "authorization_requests.csv")


# ------------------------------------------------------------ tabla y límites ---

@pytest.mark.parametrize("days,req", [
    (0.5, 0.0), (7, 0.0), (7.0001, 8.0), (14, 8.0), (14.0001, 10.0), (21, 10.0),
    (21.0001, 12.0), (28, 12.0), (28.0001, 15.0), (35, 15.0), (35.0001, 20.0), (60, 20.0), (60.0001, 50.0), (3000, 50.0)])
def test_required_return_table_has_no_overlaps(days, req):
    assert eg.required_return_pct(days) == req


@pytest.mark.parametrize("days,req", [(7, 0.0), (14, 8.0), (21, 10.0), (28, 12.0), (35, 15.0)])
def test_boundaries_are_inclusive_and_minimum_is_exact(days, req):
    if req == 0:
        assert not eg.meets_minimum(0.0, days) and eg.meets_minimum(0.001, days)
    else:
        assert eg.meets_minimum(req, days) and not eg.meets_minimum(req - 0.001, days)
    assert eg.required_return_pct(days + 1 / 86400) > req     # un segundo más: tramo siguiente


@pytest.mark.parametrize("days,ret,case", [
    (7, 0.001, "A"),          # 7 días exactos: alcanza con > 0 %
    (7.5, 0.0791, "B"),       # pasó los 7 días: 7,91 % < 8 %
    (14, 0.0799, "B"), (14, 0.0801, "A"), (21, 0.0999, "B"), (21, 0.1001, "A"),
    (28, 0.1199, "B"), (28, 0.1201, "A"), (35, 0.1499, "B"), (35, 0.1501, "A"),
    (36, 0.1999, "B"), (36, 0.2001, "A"),
    (60, 0.1999, "B"), (60, 0.2001, "A"),                              # hasta 60 días sigue el 20 %
    (60.5, 0.4999, "C"), (60.5, 0.5001, "A"),                          # más de 60: solo desorbitante
    (3000, 0.25, "C"), (3000, 0.5001, "A")])                           # y no se consulta lo que no llega
def test_entries_at_each_boundary(tmp_path, days, ret, case):
    s = store(tmp_path)
    pos, why = go(s, bundle(ret=ret), 0, legs_in(days))
    d = decisions(tmp_path)[-1]
    assert d["case"] == case
    assert (pos is not None) == (case == "A")
    if case == "B":
        assert why == "BELOW_MIN_RETURN" and s.book.cash == 100.0


def test_positive_but_below_minimum_requests_authorization_and_does_not_open(tmp_path):
    s = store(tmp_path)
    pos, why = go(s, bundle(), 0, legs_in(50))                # 15 % a 50 días: cerca del 20 % exigido
    assert pos is None and why == "BELOW_MIN_RETURN" and s.book.cash == 100.0
    q = requests(tmp_path)[-1]
    assert q["case"] == "B" and float(q["required_return_pct"]) == 20.0
    assert float(q["shortfall_pp"]) == pytest.approx(20.0 - float(q["expected_return_pct"]), abs=1e-3)
    assert int(q["contracts"]) == 8 and float(q["outlay"]) == pytest.approx(8 / 1.15, abs=1e-3)


# ------------------------------------------------------------ plazo de recupero ---

def test_recovery_uses_latest_resolution_plus_settlement_and_the_slowest_leg():
    legs = [{"ticker": "A", "status": "active", "latest_expiration_time": "2030-12-31T15:00:00Z",
             "settlement_timer_seconds": 3600},
            {"ticker": "B", "status": "active", "latest_expiration_time": "2035-12-31T15:00:00Z",
             "settlement_timer_seconds": 3600}]
    days, at, _ = eg.recovery_period(legs, "2026-10-21T12:00:00+00:00")
    assert at == "2035-12-31T16:00:00+00:00"
    assert days == pytest.approx((datetime(2035, 12, 31, 16, tzinfo=timezone.utc) - T0).total_seconds() / 86400)


@pytest.mark.parametrize("legs", [
    None,
    [{"ticker": "A", "status": "active", "settlement_timer_seconds": 0}],               # sin fecha límite
    [{"ticker": "A", "status": "active", "latest_expiration_time": "2026-11-01T00:00:00Z"}],  # sin liquidación
    [{"ticker": "A", "status": "closed", "latest_expiration_time": "2026-11-01T00:00:00Z",
      "settlement_timer_seconds": 0}],                                                   # pata no abierta
    [{"ticker": "A", "status": "active", "latest_expiration_time": "2026-10-01T00:00:00Z",
      "settlement_timer_seconds": 0}],                                                   # vencida sin liquidar
])
def test_unverifiable_period_is_case_d(tmp_path, legs):
    s = store(tmp_path)
    pos, why = go(s, bundle(ret=0.5), 0, legs)              # aun con 50 %: no se abre sola
    assert pos is None and why == eg.NOT_VERIFIABLE
    q = requests(tmp_path)[-1]
    assert q["case"] == "D" and q["recovery_days"] == "" and q["required_return_pct"] == ""


# ------------------------------------------------------------ autorizaciones ---

def test_persistent_signal_keeps_one_request_and_notifies_once(tmp_path):
    s = store(tmp_path)
    d = tmp_path / "strike_inconsistency"
    for i in range(4):
        go(s, bundle(), i, legs_in(50, i))
    assert len(requests(tmp_path)) == 1
    assert len({r["request_id"] for r in decisions(tmp_path)}) == 1
    first = build_strategy_cycle_lines(d, datetime.fromisoformat(ts(0)))
    later = build_strategy_cycle_lines(d, datetime.fromisoformat(ts(1)))
    assert first[0].startswith("Autorización requerida [") and later == []


@pytest.mark.parametrize("change,kwargs,legs_days", [
    ("precio", {"prices": (0.139, 0.829)}, 50),
    ("rentabilidad", {"ret": 0.16}, 50),
    ("liquidez", {"contracts": 4}, 50),
    ("plazo", {"ret": 0.12}, 30),                              # cambia el tramo de la tabla (20 % -> 15 %)
])
def test_material_change_replaces_request_and_invalidates_approval(tmp_path, change, kwargs, legs_days):
    s = store(tmp_path)
    go(s, bundle(), 0, legs_in(50))
    old = requests(tmp_path)[-1]["request_id"]
    approvals = {old: {"approved_at": "2026-10-21"}}
    pos, _ = go(s, bundle(**kwargs), 1, legs_in(legs_days, 1), approvals)
    assert pos is None and s.book.cash == 100.0               # la autorización vieja ya no vale
    q = requests(tmp_path)[-1]
    assert q["replaces"] == old and change in q["material_change"] and q["request_id"] != old
    lines = build_strategy_cycle_lines(tmp_path / "strike_inconsistency", datetime.fromisoformat(ts(1)))
    assert any("Cambio material" in l and old in l for l in lines)


def test_small_book_noise_is_not_material(tmp_path):
    s = store(tmp_path)
    go(s, bundle(), 0, legs_in(50))
    go(s, bundle(contracts=7), 1, legs_in(50, 1))            # −12,5 % de contratos, mismo precio
    assert len(requests(tmp_path)) == 1


def test_approved_request_opens_one_entry_once(tmp_path):
    s = store(tmp_path)
    go(s, bundle(contracts=8, avail=100.0), 0, legs_in(50))
    rid = requests(tmp_path)[-1]["request_id"]
    approvals = {rid: {"approved_at": "2026-10-21"}}
    pos, why = go(s, bundle(contracts=8, avail=100.0, prices=(0.129, 0.8391)), 1, legs_in(50, 1), approvals)
    assert why == "AUTHORIZED" and pos.contracts == 8
    e = read_csv(tmp_path / "strike_inconsistency" / "entries.csv")[-1]
    assert e["authorization_id"] == rid and e["case"] == "B"
    pos2, why2 = go(s, bundle(contracts=8, avail=100.0, prices=(0.128, 0.8391)), 2, legs_in(50, 2), approvals)
    assert pos2 is None and why2 == "BELOW_MIN_RETURN"         # otra entrada = otra solicitud
    assert requests(tmp_path)[-1]["request_id"] != rid
    assert s.book.reconcile(100.0) == pytest.approx(0.0)
    lines = build_strategy_cycle_lines(tmp_path / "strike_inconsistency", datetime.fromisoformat(ts(1)))
    assert any(l.startswith(f"Nueva entrada efectuada (autorizada [{rid}])") for l in lines)


def test_authorization_never_exceeds_authorized_contracts(tmp_path):
    s = store(tmp_path)
    go(s, bundle(contracts=8, avail=100.0), 0, legs_in(50))
    rid = requests(tmp_path)[-1]["request_id"]
    pos, _ = go(s, bundle(contracts=9, avail=100.0, prices=(0.128, 0.839)), 1, legs_in(50, 1),
                {rid: {}})
    assert pos.contracts == 8


def test_approvals_file_is_read_per_strategy(tmp_path):
    f = tmp_path / "authorizations.json"
    f.write_text(json.dumps({"strike_inconsistency": {"abc": {"approved_at": "x"}}}), encoding="utf-8")
    assert eg.load_approvals("strike_inconsistency", f) == {"abc": {"approved_at": "x"}}
    assert eg.load_approvals("buy_all_no", f) == {}
    assert eg.load_approvals("strike_inconsistency", tmp_path / "missing.json") == {}


def test_repo_authorizations_file_starts_empty():
    assert eg.load_approvals("strike_inconsistency") == {}


# ------------------------------------------------------------ caso C ---

def test_insufficient_cash_is_case_c_without_authorization_request(tmp_path):
    other = PaperPosition("X", ["a"], 1, 97.0, 0, 0, 0, "t", None)
    s = store(tmp_path, cash=3.0, open_=[other])
    d = tmp_path / "strike_inconsistency"
    for i in range(3):
        pos, why = go(s, bundle(), i, legs_in(50, i))
        assert pos is None and why == "INSUFFICIENT_CASH"
    assert not (d / "authorization_requests.csv").exists()
    assert {r["case"] for r in decisions(tmp_path)} == {"C"}
    assert sum("falta de capital" in l for l in build_strategy_cycle_lines(d, T0)) == 1  # una sola vez
    assert build_strategy_cycle_lines(d, datetime.fromisoformat(ts(1))) == []


def test_case_c_clears_a_pending_request_and_return_to_b_asks_again(tmp_path):
    s = store(tmp_path)
    go(s, bundle(contracts=8, avail=8.0), 0, legs_in(50))
    first = requests(tmp_path)[-1]["request_id"]
    s.book.open.append(PaperPosition("USCLIMATE", ["USCLIMATE-2025", "USCLIMATE-2030"], 8, 7.7, 0.1, 0.1,
                                     0.1, ts(1), None, sides=["yes", "no"]))
    s.book.cash -= 7.9                                          # liquidez tomada por otra vía (simulado)
    _, why = go(s, bundle(contracts=8, avail=8.0), 1, legs_in(50, 1))
    assert why == "LIQUIDITY_ALREADY_TAKEN"
    s.book.open.pop(); s.book.cash += 7.9
    go(s, bundle(contracts=8, avail=8.0), 2, legs_in(50, 2))
    assert requests(tmp_path)[-1]["request_id"] != first


def test_technical_retry_does_not_create_requests_or_notifications(tmp_path):
    s = store(tmp_path)
    go(s, bundle(), 0, legs_in(50))
    go(s, bundle(), 0, legs_in(50))                          # reproceso del mismo ciclo
    assert len(requests(tmp_path)) == 1
    pos, why = go(s, bundle(), 1, legs_in(3), None)            # caso A
    _, why2 = go(s, bundle(), 1, legs_in(3), None)             # reproceso
    assert why2 == "DUPLICATE_ENTRY" and len(s.book.open) == 1
    lines = build_strategy_cycle_lines(tmp_path / "strike_inconsistency", datetime.fromisoformat(ts(1)))
    assert not any("duplicada" in l or "DUPLICATE" in l for l in lines)


# ------------------------------------------------------------ conteos y ledger ---

def test_signal_entry_position_close_realized_are_counted_separately(tmp_path):
    s = store(tmp_path)
    d = tmp_path / "strike_inconsistency"
    seq = [(bundle(avail=8.0), legs_in(3)),                            # A: entrada
           (bundle(avail=8.0), legs_in(3)),                            # liquidez propia → C
           (bundle(prices=(0.119, 0.849)), legs_in(50)),             # B: solicitud
           (bundle(prices=(0.119, 0.849)), legs_in(50))]             # misma solicitud, sin repetir
    for i, (r, legs) in enumerate(seq):
        s.log("opportunities.csv", OPPORTUNITY_FIELDS, opportunity_row(ts(i), r))
        go(s, r, i, legs if i < 2 else legs_in(50, i))
    pos = s.book.open[0]
    markets = {"USCLIMATE-2025": {"status": "finalized", "result": "yes"},
               "USCLIMATE-2030": {"status": "finalized", "result": "no"}}
    assert s.book.try_settle(pos, markets, ts(4))
    s.log("paper_trades.csv", ["timestamp", "action"], {"timestamp": ts(4), "action": "SETTLE"})
    s.save()
    daily = _strategy_daily_lines(d, T0 - timedelta(hours=1), 100.0)
    assert "señales ejecutables 4 (1 pares distintos)" in daily[0]
    assert "Solicitudes de autorización 1 (vigentes 1)" in daily[1]
    assert "entradas nuevas 1" in daily[1] and "rechazos 1" in daily[1]
    assert "Posiciones abiertas 0 en 0 pares | cierres 1" in daily[2]
    assert f"P&L realizado US${pos.realized_net:+.2f}" in daily[3]
    assert "capital bloqueado US$0.00" in daily[3]
    assert s.book.reconcile(100.0) == pytest.approx(0.0)


def test_expected_profit_is_never_presented_as_realized(tmp_path):
    s = store(tmp_path)
    d = tmp_path / "strike_inconsistency"
    go(s, bundle(), 0, legs_in(3))
    go(s, bundle(prices=(0.119, 0.849)), 1, legs_in(50, 1))
    text = "\n".join(build_strategy_cycle_lines(d, T0))
    assert "neto esperado" in text.lower() and "realizado" not in text.replace("no realizado", "")
    s.save()
    daily = _strategy_daily_lines(d, T0, 100.0)
    assert "P&L realizado US$+0.00" in daily[3] and "(no realizado)" in daily[3]


# ------------------------------------------------------------ historial y aislamiento ---

def test_existing_positions_and_history_are_preserved(tmp_path):
    legacy = [PaperPosition("USCLIMATE", ["USCLIMATE-2025", "USCLIMATE-2030"], 9, 8.712, 0.17, 0.018,
                            0.10, "2026-10-20T21:31:57+00:00", "2030-12-31T15:00Z", sides=["yes", "no"]),
              PaperPosition("KXUST10YRRATE27-27DEC31", ["T1.99", "T3.99"], 10, 9.5, 0.17, 0.02, 0.31,
                            "2026-10-18T10:53:53+00:00", "2027-12-31", sides=["yes", "no"])]
    before = [asdict(p) for p in legacy]
    s = store(tmp_path, cash=100.0 - sum(p.outlay for p in legacy), open_=legacy)
    trades = tmp_path / "strike_inconsistency" / "paper_trades.csv"
    trades.parent.mkdir(parents=True)
    trades.write_text("timestamp,action\n2026-10-20T21:31:57+00:00,OPEN\n", encoding="utf-8")
    go(s, bundle(), 0, legs_in(50))                          # B
    go(s, bundle(prices=(0.119, 0.849)), 1, legs_in(3))        # A
    assert [asdict(p) for p in s.book.open[:2]] == before    # sin cerrar ni modificar
    assert trades.read_text(encoding="utf-8").startswith("timestamp,action\n2026-10-20T21:31:57+00:00,OPEN\n")
    assert s.book.reconcile(100.0) == pytest.approx(0.0)


def test_buy_all_no_and_kalshi_current_are_isolated(tmp_path):
    s = StrategyStore(tmp_path, "buy_all_no", 100.0, max_gap_min=40)
    r = bundle()
    pos, why = open_paper(s, r, None, ts(0))
    assert why == "OPENED" and open_paper(s, r, None, ts(1)) == (None, "ALREADY_OPEN")
    d = tmp_path / "buy_all_no"
    assert not (d / "decisions.csv").exists() and not (d / "authorization_requests.json").exists()
    s.save()
    lines = build_strategy_cycle_lines(d, T0)
    assert lines and lines[0].startswith("Paper abierta: ")    # formato de siempre
    assert compose_cycle_message(tmp_path / "nada", T0) is None  # KALSHI_CURRENT sin datos: sin aviso


def test_runner_routes_only_strike_through_the_gate():
    import inspect
    import kalshi_strategies
    src = inspect.getsource(kalshi_strategies.run_strategy)
    assert "strategy == strike_inconsistency.STRATEGY and strike_inconsistency.REPEAT_ENTRIES" in src
    assert "markets=legs, approvals=approvals" in src
    from src.config import BotConfig
    assert BotConfig().paper_only is True


# ------------------------------------------------------------ muy lejos del mínimo ---

def test_far_below_minimum_is_discarded_without_asking_or_notifying(tmp_path):
    s = store(tmp_path)
    d = tmp_path / "strike_inconsistency"
    for i in range(3):                                           # USCLIMATE: 1,1 % a ~3.000 días (mínimo 50 %)
        pos, why = go(s, bundle(ret=0.0111), i, legs_in(3358, i))
        assert pos is None and why == "FAR_BELOW_MIN_RETURN" and s.book.cash == 100.0
    assert not (d / "authorization_requests.csv").exists()
    assert {r["case"] for r in decisions(tmp_path)} == {"C"}
    assert build_strategy_cycle_lines(d, T0) == []               # ni pedido ni aviso
    s.save()
    daily = _strategy_daily_lines(d, T0 - timedelta(hours=1), 100.0)
    assert "Solicitudes de autorización 0" in daily[1] and "entradas nuevas 0" in daily[1]
    assert "debajo del mínimo (sin pedir autorización): 3" in daily[1] and "rechazos 0" in daily[1]


def test_far_below_minimum_clears_a_pending_request(tmp_path):
    s = store(tmp_path)
    go(s, bundle(), 0, legs_in(50))                            # 30 %: cerca, pide
    go(s, bundle(ret=0.0111), 1, legs_in(50, 1))               # cae muy abajo
    from src.strategies.entry_gate import PendingRequests
    assert PendingRequests(tmp_path / "strike_inconsistency" / "authorization_requests.json").pending == {}


def test_over_60_days_only_exorbitant_returns_and_never_asks(tmp_path):
    s = store(tmp_path)
    for i, (days, ret) in enumerate([(61, 0.30), (365, 0.49), (3358, 0.30)]):    # 30 % ya no alcanza pasados 60 días
        pos, why = go(s, bundle(ret=ret), i, legs_in(days, i))
        assert pos is None and why == "FAR_BELOW_MIN_RETURN"
    assert not (tmp_path / "strike_inconsistency" / "authorization_requests.csv").exists()
    pos, why = go(s, bundle(ret=0.60, prices=(0.14, 0.82)), 3, legs_in(3358, 3))  # desorbitante: se abre sola
    assert pos is not None and decisions(tmp_path)[-1]["case"] == "A"
