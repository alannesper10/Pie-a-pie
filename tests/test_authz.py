"""Autorizar / rechazar desde la notificación de ntfy (solo paper)."""

import json
from datetime import datetime, timedelta, timezone

import pytest
import requests

from src import authz, notify
from src.notify import authz_notifications, build_strategy_cycle_lines, compose_cycle_message, _strategy_daily_lines
from src.strategies import entry_gate as eg
from src.strategies.kalshi_common import StrategyStore, open_paper_repeat
from src.tracking import read_csv

from tests.test_entry_gate import KEY, T0, bundle, legs_in, ts

KEYSEC = "k" * 64
STRAT = "strike_inconsistency"
ENV = {"NTFY_TOPIC": "mi-topic", authz.KEY_ENV: KEYSEC}


def store(tmp_path):
    s = StrategyStore(tmp_path / "strategies", STRAT, 100.0, max_gap_min=40)
    return s


def go(s, i, markets=None, approvals=None, **kw):
    return open_paper_repeat(s, bundle(**kw), "2030-12-31T15:00:00Z", ts(i), starting_cash=100.0,
                             max_key_outlay=25.0, reference_rate=0.04,
                             markets=markets or legs_in(3358, i), approvals=approvals)


def request_id(s):
    return eg.PendingRequests(s.dir / "authorization_requests.json").pending[KEY]["request_id"]


def tap(rid, decision, exp=None, key=KEYSEC, strategy=STRAT, mid="m1"):
    exp = exp if exp is not None else (T0 + timedelta(hours=20)).timestamp()
    return {"id": mid, "event": "message", "message": authz.make_token(key, strategy, rid, decision, exp)}


def apply(s, msgs, hours=1):
    return authz.apply_messages(STRAT, s.dir, msgs, KEYSEC, T0 + timedelta(hours=hours))


def events(s):
    return read_csv(s.dir / "authorization_events.csv")


def decisions(s):
    return read_csv(s.dir / "decisions.csv")


def entries(s):
    return read_csv(s.dir / "entries.csv")


# ---------------------------------------------------------------- tokens ---

def test_token_roundtrip_and_tampering():
    t = authz.make_token(KEYSEC, STRAT, "abc123", "A", 1_800_000_000)
    assert authz.parse_token(KEYSEC, t) == (STRAT, "abc123", "A", 1_800_000_000)
    assert authz.parse_token("otra-clave", t) is None
    assert authz.parse_token(KEYSEC, t.replace(".A.", ".R.")) is None          # cambiar la decisión
    assert authz.parse_token(KEYSEC, t.replace("abc123", "abc124")) is None    # otra solicitud
    assert authz.parse_token(KEYSEC, t.replace(".1800000000.", ".1900000000.")) is None  # alargar la vida
    assert authz.parse_token(KEYSEC, t.replace(STRAT, "buy_all_no")) is None
    for junk in ("", "hola", "v1.a.b.A.x.y", "v2.a.b.A.1.2", None):
        assert authz.parse_token(KEYSEC, junk) is None
    assert authz.parse_token("", t) is None


def test_buttons_carry_no_secret_and_only_a_scoped_token():
    acts = authz.action_buttons(KEYSEC, STRAT, "abc123", "2026-10-21T12:00:00+00:00", "mi-topic-authz")
    assert [a["label"] for a in acts] == ["Autorizar", "Rechazar"]
    for a in acts:
        assert a["action"] == "http" and a["method"] == "POST" and a["url"] == "https://ntfy.sh/mi-topic-authz"
        assert KEYSEC not in json.dumps(a)
        assert authz.parse_token(KEYSEC, a["body"])[1] == "abc123"
    assert {authz.parse_token(KEYSEC, a["body"])[2] for a in acts} == {"A", "R"}
    exp = authz.parse_token(KEYSEC, acts[0]["body"])[3]
    assert exp == int(datetime(2026, 10, 22, 12, tzinfo=timezone.utc).timestamp())      # 24 h


def test_reply_topic_defaults_and_override():
    assert authz.reply_topic({"NTFY_TOPIC": "x"}) == "x-authz"
    assert authz.reply_topic({"NTFY_TOPIC": "x", "NTFY_REPLY_TOPIC": "otro"}) == "otro"
    assert authz.reply_topic({}) == ""


# ---------------------------------------------------------------- autorizar ---

def test_authorize_opens_exactly_one_paper_entry_after_fresh_check(tmp_path):
    s = store(tmp_path)
    go(s, 0, contracts=8, avail=100.0)
    rid = request_id(s)
    evs = apply(s, [tap(rid, "A")])
    assert [e["event"] for e in evs] == ["ACCEPTED"] and not entries(s)         # registrar no abre nada
    pos, why = go(s, 1, contracts=8, avail=100.0)                               # ciclo siguiente, mismo precio
    assert why == "AUTHORIZED" and pos.contracts == 8 and len(entries(s)) == 1
    assert entries(s)[0]["authorization_id"] == rid
    assert s.book.reconcile(100.0) == pytest.approx(0.0)
    pos2, why2 = go(s, 2, contracts=8, avail=100.0)                             # no vale para otra entrada
    assert pos2 is None and len(entries(s)) == 1
    assert rid in eg.PendingRequests(s.dir / "authorization_requests.json").used
    assert any(e["event"] == "EXECUTED" for e in events(s))


def test_authorization_never_exceeds_requested_contracts_and_stays_paper(tmp_path):
    s = store(tmp_path)
    go(s, 0, contracts=8, avail=100.0)
    rid = request_id(s)
    apply(s, [tap(rid, "A")])
    pos, _ = go(s, 1, contracts=9, avail=100.0)                                 # +12 %: no es cambio material
    assert pos.contracts == 8
    s2 = store(tmp_path / "otro")
    go(s2, 0, contracts=8, avail=100.0)
    apply(s2, [tap(request_id(s2), "A")])
    pos2, _ = go(s2, 1, contracts=12, avail=100.0)                              # +50 %: pide de nuevo
    assert pos2 is None and not entries(s2)
    from src.config import BotConfig
    assert BotConfig().paper_only is True


def test_quote_change_between_tap_and_cycle_cancels_authorization(tmp_path):
    s = store(tmp_path)
    go(s, 0, avail=100.0)
    rid = request_id(s)
    apply(s, [tap(rid, "A")])
    pos, why = go(s, 1, avail=100.0, prices=(0.14, 0.82))                       # precio materialmente distinto
    assert pos is None and s.book.cash == 100.0 and not entries(s)
    ev = [e for e in events(s) if e["event"] == "CONDITIONS_CHANGED"]
    assert len(ev) == 1 and ev[0]["request_id"] == rid and "precio" in ev[0]["detail"]
    new = request_id(s)
    assert new != rid
    pos2, _ = go(s, 2, avail=100.0, prices=(0.14, 0.82))                        # y la vieja no abre la nueva
    assert pos2 is None
    lines = build_strategy_cycle_lines(s.dir, T0 + timedelta(minutes=40), authz_separate=True)
    assert any("condiciones modificadas" in l for l in lines)


def test_authorization_respects_cash_liquidity_and_ledger(tmp_path):
    s = store(tmp_path)
    go(s, 0, avail=100.0)
    rid = request_id(s)
    apply(s, [tap(rid, "A")])
    from src.paper_trader import PaperPosition
    s.book.open.append(PaperPosition("X", ["a"], 1, 97.0, 0, 0, 0, "t", None))   # capital ocupado por otra posición
    s.book.cash = 3.0
    pos, why = go(s, 1, avail=100.0)
    assert pos is None and why == "INSUFFICIENT_CASH" and not entries(s)
    assert any(e["event"] == "CONDITIONS_CHANGED" for e in events(s))


def test_authorization_does_not_touch_existing_positions(tmp_path):
    from src.paper_trader import PaperBook, PaperPosition
    s = store(tmp_path)
    legacy = PaperPosition("USCLIMATE", ["USCLIMATE-2025", "USCLIMATE-2030"], 9, 8.712, 0.17, 0.018,
                           0.10, "2026-10-20T21:31:57+00:00", "2030-12-31T15:00Z", sides=["yes", "no"])
    s.book = PaperBook(cash=100.0 - legacy.outlay, open=[legacy])
    before = legacy.__dict__.copy()
    go(s, 0, avail=100.0)
    apply(s, [tap(request_id(s), "A")])
    go(s, 1, avail=100.0)
    assert s.book.open[0] is legacy and legacy.__dict__ == before and len(s.book.open) == 2


# ---------------------------------------------------------------- rechazar ---

def test_reject_is_recorded_and_not_asked_again_for_same_condition(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    evs = apply(s, [tap(rid, "R")])
    assert [e["event"] for e in evs] == ["REJECTED"]
    for i in (1, 2, 3):
        pos, why = go(s, i)
        assert pos is None and decisions(s)[-1]["decision"] == "REJECTED_BY_USER"
    assert len(read_csv(s.dir / "authorization_requests.csv")) == 1             # ni una solicitud más
    lines = build_strategy_cycle_lines(s.dir, T0 + timedelta(minutes=40), authz_separate=False)
    assert not any("Autorización requerida" in l or "Sin nueva entrada" in l for l in lines)
    assert s.book.cash == 100.0 and not entries(s)


def test_reject_then_materially_different_opportunity_asks_again(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    apply(s, [tap(rid, "R")])
    go(s, 1)
    go(s, 2, prices=(0.14, 0.82))                                               # cotización distinta
    reqs = read_csv(s.dir / "authorization_requests.csv")
    assert len(reqs) == 2 and reqs[-1]["replaces"] == rid and "precio" in reqs[-1]["material_change"]
    assert request_id(s) != rid


def test_reject_then_tap_authorize_is_ignored_with_notice(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    apply(s, [tap(rid, "R", mid="a")])
    evs = apply(s, [tap(rid, "A", mid="b")], hours=2)
    assert [e["event"] for e in evs] == ["CONFLICT"] and evs[0]["detail"] == "rechazada"
    pos, _ = go(s, 3)
    assert pos is None and not entries(s)


# ---------------------------------------------------------------- idempotencia ---

def test_double_tap_and_retries_record_one_decision_and_one_entry(tmp_path):
    s = store(tmp_path)
    go(s, 0, contracts=8, avail=100.0)
    rid = request_id(s)
    batch = [tap(rid, "A", mid="a"), tap(rid, "A", mid="b"), tap(rid, "A", mid="c")]
    evs = apply(s, batch)
    assert [e["event"] for e in evs] == ["ACCEPTED"]                            # una sola aceptación
    assert apply(s, batch, hours=2) == []                                       # reproceso del buzón
    go(s, 1, contracts=8, avail=100.0)
    go(s, 2, contracts=8, avail=100.0)
    assert len(entries(s)) == 1 and len(s.book.open) == 1
    assert apply(s, batch, hours=3) == []                                       # tocar tras ejecutarse
    assert len(entries(s)) == 1
    d = json.loads((s.dir / "authorization_requests.json").read_text(encoding="utf-8"))
    assert list(d["decisions"]) == [rid]


# ---------------------------------------------------------------- vigencia ---

def test_expired_token_is_reported_and_request_is_reissued(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    old = (T0 - timedelta(hours=1)).timestamp()
    evs = apply(s, [tap(rid, "A", exp=old)])
    assert [e["event"] for e in evs] == ["EXPIRED"]
    pos, _ = go(s, 1)
    assert pos is None and request_id(s) != rid                                 # pedido nuevo con botones nuevos
    assert len(read_csv(s.dir / "authorization_requests.csv")) == 2


def test_unanswered_request_expires_after_ttl(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    evs = apply(s, [], hours=25)
    assert [e["event"] for e in evs] == ["EXPIRED"] and evs[0]["detail"] == "sin respuesta en 24 h"
    assert eg.PendingRequests(s.dir / "authorization_requests.json").pending == {}


def test_stale_request_replaced_by_material_change(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    old = request_id(s)
    go(s, 1, prices=(0.14, 0.82))                                               # reemplaza la solicitud
    evs = apply(s, [tap(old, "A")])
    assert [e["event"] for e in evs] == ["STALE"]
    pos, _ = go(s, 2, prices=(0.14, 0.82))
    assert pos is None and not entries(s)


def test_unknown_request_id_is_stale_and_changes_nothing(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    evs = apply(s, [tap("noexiste", "A")])
    assert [e["event"] for e in evs] == ["STALE"]
    pos, _ = go(s, 1)
    assert pos is None and not entries(s)


def test_forged_or_foreign_messages_are_ignored(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    msgs = [tap(rid, "A", key="clave-falsa", mid="1"), tap(rid, "A", strategy="buy_all_no", mid="2"),
            {"id": "3", "event": "message", "message": "autorizar todo"},
            {"id": "4", "event": "message", "message": ""}]
    assert apply(s, msgs) == []
    assert eg.PendingRequests(s.dir / "authorization_requests.json").cursor == "4"
    pos, _ = go(s, 1)
    assert pos is None and not entries(s)


def test_authorization_does_not_carry_over_to_other_pairs(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    apply(s, [tap(rid, "A")])
    other = bundle()
    object.__setattr__(other, "key", "OTRO-A|OTRO-B")
    pos, _ = open_paper_repeat(s, other, None, ts(1), starting_cash=100.0, max_key_outlay=25.0,
                               reference_rate=0.04, markets=legs_in(3358, 1))
    assert pos is None                                                          # su propia solicitud, no la tuya


# ---------------------------------------------------------------- comunicación ---

class Resp:
    def __init__(self, text="", status=200):
        self.text, self.status_code = text, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("x")


class Http:
    def __init__(self, *resps):
        self.resps, self.calls = list(resps), []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        r = self.resps.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def test_fetch_parses_only_messages_and_keeps_topic_out_of_errors():
    body = "\n".join([json.dumps({"id": "1", "event": "open"}), "basura",
                      json.dumps({"id": "2", "event": "message", "message": "x"})])
    assert [m["id"] for m in authz.fetch("t", http=Http(Resp(body)))] == ["2"]
    with pytest.raises(authz.FetchError) as ei:
        authz.fetch("secreto-topic", http=Http(requests.ConnectionError("http://ntfy.sh/secreto-topic")))
    assert "secreto-topic" not in str(ei.value)
    with pytest.raises(authz.FetchError):
        authz.fetch("t", http=Http(Resp("", 500)))


def test_stale_cursor_falls_back_to_full_read():
    http = Http(Resp("", 400), Resp(json.dumps({"id": "9", "event": "message", "message": "x"})))
    assert len(authz.fetch("t", since="viejo", http=http)) == 1
    assert http.calls[1][1]["since"] == "all"


def test_communication_error_keeps_cursor_and_retries_next_cycle(tmp_path):
    s = store(tmp_path)
    go(s, 0, avail=100.0)
    rid = request_id(s)
    root = s.dir.parent

    def boom(topic, cursor):
        raise authz.FetchError("ConnectionError")

    assert authz.poll((STRAT,), ENV, T0 + timedelta(hours=1), root, boom) == []
    assert eg.PendingRequests(s.dir / "authorization_requests.json").decisions == {}
    ok = lambda topic, cursor: [tap(rid, "A")]                                  # noqa: E731
    evs = authz.poll((STRAT,), ENV, T0 + timedelta(hours=2), root, ok)
    assert [e["event"] for e in evs] == ["ACCEPTED"]


def test_poll_without_key_or_topic_does_nothing(tmp_path):
    assert authz.poll((STRAT,), {}, root=tmp_path, fetch_fn=lambda *a: pytest.fail("no debe leer")) == []
    assert authz.poll((STRAT,), {"NTFY_TOPIC": "x"}, root=tmp_path,
                      fetch_fn=lambda *a: pytest.fail("no debe leer")) == []


def test_poll_uses_stored_cursor(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    seen = []

    def fake(topic, cursor):
        seen.append((topic, cursor))
        return [{"id": "z9", "event": "message", "message": "nada"}]

    authz.poll((STRAT,), ENV, T0, s.dir.parent, fake)
    authz.poll((STRAT,), ENV, T0, s.dir.parent, fake)
    assert seen == [("mi-topic-authz", None), ("mi-topic-authz", "z9")]


def test_send_failure_never_raises(monkeypatch):
    def boom(*a, **k):
        raise requests.ConnectionError("fallo")
    monkeypatch.setattr(notify.requests, "post", boom)
    assert notify.send("t", "titulo", "cuerpo", actions=[{"action": "http", "label": "x"}]) is False
    assert authz.send_test(ENV, post=boom) is False


# ---------------------------------------------------------------- notificaciones ---

def test_request_notification_has_buttons_and_payload_has_no_secret(tmp_path, monkeypatch):
    s = store(tmp_path)
    go(s, 0)
    s.save()
    out = authz_notifications(tmp_path, T0, ENV)
    assert len(out) == 1
    title, body, prio, tags, actions = out[0]
    assert title.startswith("[STRIKE_INCONSISTENCY]") and "Tocá Autorizar o Rechazar" in body
    assert [a["label"] for a in actions] == ["Autorizar", "Rechazar"] and request_id(s) in body
    sent = {}
    monkeypatch.setattr(notify.requests, "post",
                        lambda url, json=None, timeout=None: sent.update(url=url, payload=json) or Resp())
    assert notify.send("mi-topic", title, body, prio, tags, actions=actions) is True
    assert KEYSEC not in __import__("json").dumps(sent["payload"]) and KEYSEC not in sent["url"]
    assert sent["payload"]["actions"] == actions


def test_without_signing_key_falls_back_to_manual_instruction(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    title, body, _, _, actions = authz_notifications(tmp_path, T0, {"NTFY_TOPIC": "t"})[0]
    assert actions is None and "config/authorizations.json" in body


def test_request_goes_in_its_own_notification_not_in_the_cycle_message(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    s.save()
    assert compose_cycle_message(tmp_path, T0 - timedelta(seconds=1), authz_separate=True) is None
    m = compose_cycle_message(tmp_path, T0 - timedelta(seconds=1))
    assert m and "Autorización requerida" in m[1]                               # modo anterior intacto


def test_confirmations_cover_accept_reject_expire_stale_and_daily_counts(tmp_path):
    s = store(tmp_path)
    go(s, 0)
    rid = request_id(s)
    apply(s, [tap(rid, "R", mid="1"), tap("viejo", "A", mid="2")])
    apply(s, [tap(rid, "A", mid="3")], hours=2)
    s.save()
    lines = build_strategy_cycle_lines(s.dir, T0, authz_separate=True)
    text = "\n".join(lines)
    assert f"Rechazo registrado [{rid}]" in text and "sin vigencia" in text and "ya estaba rechazada" in text
    daily = _strategy_daily_lines(s.dir, T0 - timedelta(hours=1), 100.0)
    assert "autorizadas 0, rechazadas 1, vencidas 0" in daily[1]


def test_authz_test_button_roundtrip_changes_nothing(tmp_path):
    sent = {}

    def post(url, json=None, timeout=None):
        sent.update(payload=json)
        return Resp()

    assert authz.send_test(ENV, post=post) is True
    acts = sent["payload"]["actions"]
    msg = {"id": "t1", "event": "message", "message": acts[0]["body"]}
    d = tmp_path / STRAT
    evs = authz.apply_messages(STRAT, d, [msg, dict(msg, id="t2")], KEYSEC, datetime.now(timezone.utc))
    assert [e["event"] for e in evs] == ["TEST_OK"]
    reqs = eg.PendingRequests(d / "authorization_requests.json")
    assert reqs.approved() == {} and reqs.pending == {} and reqs.used == []
