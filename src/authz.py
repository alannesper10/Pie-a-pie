"""Autorizar o rechazar solicitudes desde la notificación de ntfy (solo paper).

Los botones de la notificación hacen un POST a un tópico buzón (<NTFY_TOPIC>-authz)
con un token firmado; este módulo, dentro del ciclo de `scan`, lee el buzón,
verifica cada token y registra la decisión. La entrada la abre el gate de siempre
(entry_gate / open_paper_repeat) con cotizaciones frescas: este módulo nunca abre
posiciones ni envía órdenes.

Token:  v1.<estrategia>.<id solicitud>.<A|R>.<vence unix>.<firma>
Firma:  HMAC-SHA256(PIEAPIE_AUTHZ_HMAC_KEY, "v1|estrategia|id|decisión|vence")[:40]
La clave vive solo como secreto de GitHub: no viaja en la notificación. Cada token
vale para una decisión sobre una solicitud y vence con ella (24 h).

Uso:  python -m src.authz poll    (lo corre el workflow scan antes de las estrategias)
      python -m src.authz test    (notificación de prueba con botones; no afecta nada)
"""

import argparse
import hmac
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from .strategies import entry_gate as eg
from .tracking import append_csv

NTFY_URL = "https://ntfy.sh"
KEY_ENV = "PIEAPIE_AUTHZ_HMAC_KEY"
STRATEGIES = ("strike_inconsistency",)
DATA = Path("data") / "strategies"
TEST_PREFIX = "prueba"


class FetchError(Exception):
    """El buzón no se pudo leer (red, HTTP): se reintenta en el próximo ciclo."""


# ---------------------------------------------------------------- tokens ---

def _sig(key, strategy, rid, decision, exp):
    msg = f"v1|{strategy}|{rid}|{decision}|{exp}".encode()
    return hmac.new(key.encode(), msg, hashlib.sha256).hexdigest()[:40]


def make_token(key, strategy, rid, decision, exp):
    return f"v1.{strategy}.{rid}.{decision}.{int(exp)}.{_sig(key, strategy, rid, decision, int(exp))}"


def parse_token(key, token):
    """-> (strategy, rid, decision, exp) si la firma es válida; None si no."""
    parts = str(token).strip().split(".")
    if len(parts) != 6 or parts[0] != "v1" or parts[3] not in ("A", "R") or not key:
        return None
    _, strategy, rid, decision, exp, sig = parts
    try:
        exp = int(exp)
    except ValueError:
        return None
    if not hmac.compare_digest(sig, _sig(key, strategy, rid, decision, exp)):
        return None
    return strategy, rid, decision, exp


def reply_topic(env=os.environ):
    explicit = env.get("NTFY_REPLY_TOPIC", "").strip()
    base = env.get("NTFY_TOPIC", "").strip()
    return explicit or (f"{base}-authz" if base else "")


def request_expiry(since_iso):
    """Vencimiento (unix) de una solicitud creada en since_iso."""
    return int((datetime.fromisoformat(since_iso) + timedelta(hours=eg.AUTHZ_TTL_H)).timestamp())


def action_buttons(key, strategy, rid, since_iso, topic, base=NTFY_URL):
    """Acciones `http` de ntfy. La URL solo lleva el tópico buzón; la autoridad está
    en el token firmado del cuerpo (una solicitud, una decisión, 24 h)."""
    exp = request_expiry(since_iso)
    return [{"action": "http", "label": label, "url": f"{base}/{topic}", "method": "POST",
             "body": make_token(key, strategy, rid, d, exp), "clear": True}
            for label, d in (("Autorizar", "A"), ("Rechazar", "R"))]


# ---------------------------------------------------------------- buzón ---

def fetch(topic, since=None, base=NTFY_URL, timeout=15, http=requests):
    """Mensajes del buzón posteriores a `since` (id de mensaje) -> [{id, time, message}]."""
    url = f"{base}/{topic}/json"
    try:
        r = http.get(url, params={"poll": "1", "since": since or "all"}, timeout=timeout)
        if since and r.status_code in (400, 404):         # cursor viejo: se relee todo (es idempotente)
            r = http.get(url, params={"poll": "1", "since": "all"}, timeout=timeout)
        r.raise_for_status()
    except requests.RequestException as e:
        raise FetchError(type(e).__name__) from None      # sin URL: contiene el tópico
    out = []
    for line in r.text.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if isinstance(m, dict) and m.get("event") == "message":
            out.append(m)
    return out


# ---------------------------------------------------------------- aplicar ---

def _iso(now):
    return now.isoformat(timespec="seconds")


def apply_messages(strategy, strategy_dir, messages, key, now):
    """Registra las decisiones válidas. Idempotente: un id se resuelve una sola vez.
    Devuelve la lista de eventos generados."""
    d = Path(strategy_dir)
    reqs = eg.PendingRequests(d / "authorization_requests.json")
    events = []

    def log(row):
        append_csv(d / "authorization_events.csv", eg.EVENT_FIELDS, row)
        events.append(row)

    ts = _iso(now)
    for m in messages:
        reqs.cursor = m.get("id") or reqs.cursor
        tok = parse_token(key, m.get("message", ""))
        if tok is None or tok[0] != strategy:
            continue                                        # firma inválida / otra estrategia: se ignora
        _, rid, decision, exp = tok
        prior = reqs.decisions.get(rid)
        if prior:                                           # doble pulsación o toque contradictorio
            if prior["decision"] != decision:
                log(eg.event_row(ts, rid, "CONFLICT", "",
                                 "autorizada" if prior["decision"] == "A" else "rechazada"))
            continue
        if rid.startswith(TEST_PREFIX):
            reqs.decisions[rid] = {"decision": decision, "status": "TEST", "at": ts}
            log(eg.event_row(ts, rid, "TEST_OK", "", "autorizar" if decision == "A" else "rechazar"))
            continue
        key_, cur = reqs.find(rid)
        if exp < now.timestamp():
            reqs.decisions[rid] = {"decision": decision, "status": "EXPIRED", "at": ts}
            if cur:
                reqs.pending.pop(key_)                      # el próximo ciclo la vuelve a pedir con botones nuevos
            log(eg.event_row(ts, rid, "EXPIRED", key_ or "", "el toque llegó después del vencimiento"))
        elif cur is None:
            reqs.decisions[rid] = {"decision": decision, "status": "STALE", "at": ts}
            log(eg.event_row(ts, rid, "STALE", "", "solicitud reemplazada, resuelta o sin vigencia"))
        elif decision == "A":
            reqs.decisions[rid] = {"decision": "A", "status": "APPROVED", "at": ts, "key": key_}
            log(eg.event_row(ts, rid, "ACCEPTED", key_, ""))
        else:
            reqs.pending.pop(key_)
            reqs.rejected[key_] = {"request_id": rid, "snapshot": cur["snapshot"], "at": ts}
            reqs.decisions[rid] = {"decision": "R", "status": "REJECTED", "at": ts, "key": key_}
            log(eg.event_row(ts, rid, "REJECTED", key_, ""))

    ttl = timedelta(hours=eg.AUTHZ_TTL_H)
    for key_, cur in list(reqs.pending.items()):             # vencen aunque nadie toque
        try:
            old = datetime.fromisoformat(cur["since"]) + ttl < now
        except (KeyError, ValueError):
            old = False
        if old:
            reqs.pending.pop(key_)
            info = reqs.decisions.get(cur["request_id"])
            if info and info.get("status") == "APPROVED":
                info["status"] = "EXPIRED"
            log(eg.event_row(ts, cur["request_id"], "EXPIRED", key_, "sin respuesta en 24 h"))
    reqs.save()
    return events


def poll(strategies=STRATEGIES, env=os.environ, now=None, root=DATA, fetch_fn=fetch):
    """Lee el buzón y aplica las decisiones. Nunca levanta: un error de red deja el
    cursor donde estaba y se reintenta en el próximo ciclo."""
    key = env.get(KEY_ENV, "").strip()
    topic = reply_topic(env)
    if not key or not topic:
        print("Autorización por celular desactivada (falta clave o tópico).")
        return []
    now = now or datetime.now(timezone.utc)
    events = []
    for strategy in strategies:
        d = Path(root) / strategy
        cursor = eg.PendingRequests(d / "authorization_requests.json").cursor
        try:
            messages = fetch_fn(topic, cursor)
        except FetchError as e:
            print(f"No se pudo leer el buzón de autorizaciones ({e}); se reintenta en el próximo ciclo.")
            continue
        events += apply_messages(strategy, d, messages, key, now)
    print(f"Autorizaciones: {len(events)} evento(s).")
    return events


def send_test(env=os.environ, base=NTFY_URL, post=requests.post):
    """Notificación de prueba con botones: verifica el camino completo sin tocar nada."""
    key, topic, main = env.get(KEY_ENV, "").strip(), reply_topic(env), env.get("NTFY_TOPIC", "").strip()
    if not (key and topic and main):
        print("Faltan NTFY_TOPIC o la clave: no se envía la prueba.")
        return False
    rid = f"{TEST_PREFIX}{int(datetime.now(timezone.utc).timestamp())}"
    exp = int((datetime.now(timezone.utc) + timedelta(hours=eg.AUTHZ_TTL_H)).timestamp())
    actions = [{"action": "http", "label": lab, "url": f"{base}/{topic}", "method": "POST",
                "body": make_token(key, STRATEGIES[0], rid, dec, exp), "clear": True}
               for lab, dec in (("Autorizar", "A"), ("Rechazar", "R"))]
    try:
        post(base, json={"topic": main, "title": "Pie a pie: prueba de botones",
                         "message": "Prueba: tocá cualquiera. No autoriza ni rechaza nada real; "
                                    "en el próximo ciclo llega la confirmación.",
                         "priority": 3, "tags": ["white_check_mark"], "actions": actions},
             timeout=10).raise_for_status()
    except requests.RequestException as e:
        print(f"No se pudo enviar la prueba ({type(e).__name__}).")
        return False
    print("Prueba enviada.")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kind", choices=["poll", "test"])
    args = p.parse_args(argv)
    if args.kind == "poll":
        poll()
    else:
        send_test()
    return 0


if __name__ == "__main__":
    sys.exit(main())
