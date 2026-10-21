"""Notificaciones push vía ntfy.sh para el workflow de Actions.

Solo lee data/ y publica un mensaje corto. No toca la API de Kalshi ni envía
órdenes. El topic sale de la variable de entorno NTFY_TOPIC (secret de
GitHub); si no está definida no se notifica y se sale sin error.

  python -m src.notify cycle --since 2026-10-07T17:00:00+00:00
  python -m src.notify daily
  python -m src.notify test
  (--dry-run imprime el mensaje en vez de enviarlo)
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from .config import BotConfig
from .paper_trader import PaperBook
from .tracking import load_json, read_csv

NTFY_URL = "https://ntfy.sh"
DATA = Path("data")


def _ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def rows_since(rows, since):
    return [r for r in rows if (t := _ts(r.get("timestamp"))) and t >= since]


def _money(value):
    try:
        return f"US${float(value):+.2f}"
    except (TypeError, ValueError):
        return "n/d"


def failed_steps(outcomes):
    """'tests=success scan=failure' -> ['scan']"""
    pairs = (p.split("=", 1) for p in (outcomes or "").split() if "=" in p)
    return [step for step, result in pairs if result == "failure"]


def build_cycle_message(data_dir, since, job_status="success", outcomes=""):
    """(title, body, priority, tags) o None si no hay nada que avisar.

    Avisa solo si: hubo ejecutables, se abrió o cerró una posición paper, o la
    corrida falló. Los casi-aciertos no notifican.
    """
    d = Path(data_dir)
    cycles = rows_since(read_csv(d / "cycles.csv"), since)
    exe = [r for r in rows_since(read_csv(d / "near_misses.csv"), since)
           if r.get("executable") == "True"]
    trades = rows_since(read_csv(d / "paper_trades.csv"), since)

    errors = [r.get("error", "") for r in cycles if r.get("ok") == "0"]
    if job_status != "success" or errors:
        steps = failed_steps(outcomes)
        lines = [f"Paso: {', '.join(steps)}" if steps else "La corrida no terminó bien."]
        if errors and errors[-1]:
            lines.append(f"Error: {errors[-1][:120]}")
        return "Pie a pie: falló el ciclo", "\n".join(lines), 3, ["warning"]

    lines = []
    for r in exe:
        lines.append(f"Ejecutable: {r['event_ticker']} ({r['n_legs']} patas, "
                     f"suma {float(r['ask_sum']):.2f}, neto {_money(r['est_net'])})")
    for r in trades:
        if r.get("action") == "OPEN":
            lines.append(f"Paper abierta: {r['event_ticker']}, {r['contracts']} "
                         f"contratos, neto esp. {_money(r['expected_net'])}")
        elif r.get("action") == "SETTLE":
            lines.append(f"Paper cerrada: {r['event_ticker']}, neto "
                         f"{_money(r['realized_net'])}")
    if not lines:
        return None
    if trades:
        lines.append(f"Caja: US${float(trades[-1]['cash_after']):.2f}")
    title = "Pie a pie: oportunidad" if exe else "Pie a pie: paper"
    return title, "\n".join(lines), 4, ["moneybag"]


def build_daily_message(data_dir, now=None, starting_cash=None):
    d = Path(data_dir)
    now = now or datetime.now(timezone.utc)
    since = now - timedelta(hours=24)
    starting_cash = (BotConfig().starting_capital_usd if starting_cash is None
                     else starting_cash)
    cycles = rows_since(read_csv(d / "cycles.csv"), since)
    near = rows_since(read_csv(d / "near_misses.csv"), since)
    exe = [r for r in near if r.get("executable") == "True"]
    state = load_json(d / "state.json", {}) or {}
    book = PaperBook.from_dict(state.get("paper"), starting_cash)

    failed = sum(r.get("ok") == "0" for r in cycles)
    body = "\n".join([
        f"Ciclos 24h: {len(cycles)} ({failed} fallidos)",
        f"Casi-aciertos: {len(near)} ({len({r['event_ticker'] for r in near})} eventos)",
        f"Ejecutables: {len(exe)}",
        f"Caja: US${book.cash:.2f} (bloqueado US${book.locked:.2f})",
        f"Neto realizado: US${book.realized_net:+.2f}",
    ])
    return "Pie a pie: resumen diario", body, 2, ["bar_chart"]



# ------------------------------------------------- estrategias experimentales ---

STRATEGY_TAGS = {"buy_all_no": "BUY_ALL_NO",
                 "strike_inconsistency": "STRIKE_INCONSISTENCY"}


REJECT_LABELS = {"INSUFFICIENT_CASH": "rechazada por falta de capital",
                 "KEY_LIMIT": "posición existente al tope del par",
                 "LIQUIDITY_ALREADY_TAKEN": "posición existente; la liquidez ya la tomamos",
                 "LEDGER_MISMATCH": "RECHAZADA: el ledger no concilia"}
CASE_LABELS = {"B": "caso B: rentabilidad debajo del mínimo por plazo",
               "D": "caso D: plazo de recupero no verificable"}


def _pct(value):
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return "s/d"


def _auth_request_lines(q, dec, buttons=False):
    """Solicitud de autorización: todo lo necesario para decidir, en un aviso."""
    days = f"{float(q['recovery_days']):.0f} días (hasta {q['recovery_at'][:10]})" \
        if q.get("recovery_days") else f"NO VERIFICABLE ({q.get('recovery_basis', '')})"
    req = (f"requerido {_pct(q['required_return_pct'])}, diferencia "
           f"{-float(q['shortfall_pp']):+.2f} pp") if q.get("required_return_pct") not in (None, "") \
        else "requerido: no aplicable sin plazo verificable"
    risks = ("capital inmovilizado hasta la liquidación de ambas patas; el piso de pago depende "
             "de las reglas de resolución; salida anticipada no verificada")
    lines = [f"Autorización requerida [{q['request_id']}] ({CASE_LABELS.get(q['case'], q['case'])})",
             f"  Posible NUEVA entrada: {q['key'][:60]} | {q['contracts']} contratos | capital "
             f"US${float(q['outlay']):.2f}",
             f"  Neto esperado (no realizado): {_money(q['expected_net'])} = {_pct(q['expected_return_pct'])}"
             f" | plazo de recupero {days}",
             f"  {req}",
             f"  Costos: comisiones US${float(q['fees']):.2f}, slippage US${float(q['slippage']):.2f}"
             f" | riesgos: {risks}",
             (f"  Tocá Autorizar o Rechazar (vence en 24 h; se aplica en el próximo ciclo, unos 30 min)"
              if buttons else
              f"  Para autorizar ESTA entrada: agregar \"{q['request_id']}\" en config/authorizations.json")]
    held = int(dec.get("entries_open_for_key") or 0)
    if held:
        lines.insert(2, f"  Posición existente del par (no se toca): {held} entrada(s), "
                        f"US${float(dec.get('key_outlay') or 0):.2f}")
    if q.get("replaces"):
        lines.insert(1, f"  Cambio material ({q['material_change'].replace(';', ', ')}): reemplaza "
                        f"[{q['replaces']}], que queda invalidada")
    return lines


EVENT_TEXT = {
    "ACCEPTED": "Autorización aceptada [{id}]: la entrada de papel se abre solo si las cotizaciones "
                "siguen sin cambio material, con caja, liquidez y ledger en regla",
    "REJECTED": "Rechazo registrado [{id}]: no se vuelve a pedir esta condición salvo una "
                "oportunidad materialmente distinta",
    "EXPIRED": "Solicitud vencida [{id}] ({detail}): si la oportunidad sigue, se pide de nuevo con botones nuevos",
    "STALE": "Solicitud [{id}] sin vigencia ({detail}): tu toque no tuvo efecto",
    "CONFLICT": "Solicitud [{id}] ya estaba {detail}: el toque contradictorio se ignoró",
    "CONDITIONS_CHANGED": "Autorización [{id}] sin usar, condiciones modificadas ({detail}): no se abrió ninguna entrada",
    "TEST_OK": "Prueba de botones recibida [{id}]: firma válida, el camino funciona (no se autorizó ni rechazó nada)",
}


def _authz_event_lines(d, since):
    """Confirmaciones de lo decidido desde el celular. EXECUTED no se avisa acá: lo cuenta
    la línea de la entrada efectuada."""
    lines = []
    for e in rows_since(read_csv(d / "authorization_events.csv"), since):
        text = EVENT_TEXT.get(e["event"])
        if text:
            lines.append(text.format(id=e["request_id"], detail=e.get("detail", "")))
    return lines


def _decision_lines(d, since, with_requests=True):
    """Modo con decisiones registradas (estrategias con entradas repetidas).

    Distingue: nueva entrada efectuada, solicitud de autorización (B/D), posición
    existente sin nueva entrada y rechazo técnico (C). Una señal que termina
    igual que en el ciclo anterior NO se vuelve a avisar; un cambio material de
    una solicitud sí. Los reprocesos (DUPLICATE_ENTRY) no se avisan.
    """
    all_dec = read_csv(d / "decisions.csv")
    recent = rows_since(all_dec, since)
    prev = {}
    for r in all_dec:
        t = _ts(r.get("timestamp"))
        if t and t < since and r.get("reason") != "DUPLICATE_ENTRY":
            prev[r["key"]] = (r["decision"], r["reason"])
    entries = {r["entry_id"]: r for r in read_csv(d / "entries.csv")}
    requests_ = {r["request_id"]: r for r in read_csv(d / "authorization_requests.csv")}
    lines = []
    for r in recent:
        k = r["key"][:60]
        if r.get("reason") == "DUPLICATE_ENTRY" or r["decision"] == "REJECTED_BY_USER":
            continue
        if r["decision"] == "OPENED":
            e = entries.get(r["entry_id"], {})
            how = (f"autorizada [{e.get('authorization_id')}]" if r["reason"] == "AUTHORIZED"
                   else "cumple el mínimo")
            req = e.get("required_return_pct")
            plazo = (f"plazo de recupero {float(e['recovery_days']):.0f} días, mínimo "
                     + ("> 0%" if req not in (None, "") and float(req) == 0 else _pct(req))
                     if e.get("recovery_days")
                     else "plazo no verificable")
            prior = int(r["entries_open_for_key"] or 0)
            lines.append(f"Nueva entrada efectuada ({how}): {k}, {r['contracts']} contratos, capital "
                         f"US${float(r['outlay']):.2f}, neto esperado {_money(r['expected_net'])} "
                         f"({_pct(e.get('expected_return_pct'))}) | {plazo} | "
                         + (f"se suma a {prior} entrada(s) existente(s) del par" if prior
                            else "primera entrada del par"))
        elif r["decision"] == "AUTHORIZATION_REQUIRED":
            if with_requests and r.get("new_request") == "1" and r.get("request_id") in requests_:
                lines += _auth_request_lines(requests_[r["request_id"]], r)
        elif prev.get(r["key"]) != (r["decision"], r["reason"]):
            label = REJECT_LABELS.get(r["reason"], r["reason"])
            lines.append(f"Sin nueva entrada: {k} ({label}; entradas abiertas {r['entries_open_for_key']}, "
                         f"US${float(r['key_outlay'] or 0):.2f})")
        prev[r["key"]] = (r["decision"], r["reason"])
    return lines


def build_strategy_cycle_lines(strategy_dir, since, step_failed=False, authz_separate=False):
    """Líneas importantes de UNA estrategia en esta corrida, o [] si no hay nada.

    Importante = ejecutable, paper abierta/cerrada o error. Los casi-aciertos
    y los net-positive no ejecutables van al resumen diario, no acá.
    Si la estrategia registra decisions.csv (entradas repetidas) se informan
    las decisiones en lugar de cada señal ejecutable repetida.
    """
    d = Path(strategy_dir)
    cycles = rows_since(read_csv(d / "cycles.csv"), since)
    opps = rows_since(read_csv(d / "opportunities.csv"), since)
    trades = rows_since(read_csv(d / "paper_trades.csv"), since)
    lines = []
    errors = [r.get("error", "") for r in cycles if r.get("ok") == "0"]
    if errors:
        lines.append(f"Error: {(errors[-1] or 'ciclo fallido')[:100]}")
    elif step_failed:
        lines.append("Error: falló el paso de estrategias")
    decisions_mode = (d / "decisions.csv").exists()
    if decisions_mode:
        lines += _authz_event_lines(d, since)
        lines += _decision_lines(d, since, with_requests=not authz_separate)
    else:
        for r in opps:
            if r.get("executable") == "True":
                lines.append(f"Ejecutable: {r['key'][:60]}, {r['contracts']} contratos, "
                             f"neto {_money(r['net_profit'])}")
    for r in trades:
        if r.get("action") == "OPEN" and not decisions_mode:
            lines.append(f"Paper abierta: {r['event_ticker']}, neto esp. "
                         f"{_money(r['expected_net'])}")
        elif r.get("action") == "SETTLE":
            lines.append(f"Paper cerrada: {r['event_ticker']}, neto "
                         f"{_money(r['realized_net'])}")
    if trades:
        lines.append(f"Caja: US${float(trades[-1]['cash_after']):.2f}")
    return lines


def compose_cycle_message(data_dir, since, job_status="success", outcomes="", authz_separate=False):
    """Una sola notificación por corrida con una sección por estrategia."""
    sections, priority = [], 0
    cur = build_cycle_message(data_dir, since, job_status, outcomes)
    if cur:
        sections.append(("KALSHI_CURRENT", cur[0].replace("Pie a pie: ", ""), cur[1]))
        priority = max(priority, cur[2])
    step_failed = "strategies" in failed_steps(outcomes)
    for name, tag in STRATEGY_TAGS.items():
        lines = build_strategy_cycle_lines(Path(data_dir) / "strategies" / name,
                                           since, step_failed, authz_separate)
        if lines:
            label = "error" if lines[0].startswith("Error") else "novedad"
            sections.append((tag, label, "\n".join(lines)))
            priority = max(priority, 3 if label == "error" else 4)
    if not sections:
        return None
    if len(sections) == 1:
        tag, label, body = sections[0]
        title = f"[{tag}] Pie a pie: {label}"
    else:
        title = "Pie a pie: " + ", ".join(t for t, _, _ in sections)
        body = "\n\n".join(f"[{t}] {b}" for t, _, b in sections)
    tags = ["warning"] if any(l == "error" or "falló" in l for _, l, _ in sections) else ["moneybag"]
    return title, body, priority, tags


def _strategy_daily_lines(strategy_dir, since, starting_cash):
    d = Path(strategy_dir)
    cycles = rows_since(read_csv(d / "cycles.csv"), since)
    opps = rows_since(read_csv(d / "opportunities.csv"), since)
    if not cycles and not (d / "state.json").exists():
        return ["sin datos todavía"]
    netpos = sum(1 for r in opps if float(r.get("net_profit") or 0) > 0
                 and float(r.get("max_contracts_available") or 0) >= 1
                 and r.get("reason") != "SUSPICIOUS_EDGE_CHECK_RULES")
    exe = sum(r.get("executable") == "True" for r in opps)
    book = PaperBook.from_dict((load_json(d / "state.json", {}) or {}).get("paper"),
                               starting_cash)
    failed = sum(r.get("ok") == "0" for r in cycles)
    if (d / "decisions.csv").exists():
        decs = rows_since(read_csv(d / "decisions.csv"), since)
        trades = rows_since(read_csv(d / "paper_trades.csv"), since)
        signals = [r for r in opps if r.get("executable") == "True"]
        pairs = {(p.key or p.event_ticker) for p in book.open}
        real = [r for r in decs if r.get("reason") != "DUPLICATE_ENTRY"]
        pending = (load_json(d / "authorization_requests.json", {}) or {}).get("pending", {})
        expected = sum(p.expected_net for p in book.open)
        events = rows_since(read_csv(d / "authorization_events.csv"), since)

        def ev(kind):
            return sum(e["event"] == kind for e in events)
        rejections, last = 0, {}                  # episodios, no filas: un rechazo que persiste cuenta 1
        for r in real:
            state = (r["decision"], r["reason"])
            rejections += r["decision"] == "REJECTED" and last.get(r["key"]) != state
            last[r["key"]] = state
        return [f"Ciclos {len(cycles)} ({failed} fallidos) | señales ejecutables {len(signals)} "
                f"({len({r['key'] for r in signals})} pares distintos)",
                f"Solicitudes de autorización {sum(r.get('new_request') == '1' for r in real)} "
                f"(vigentes {len(pending)}) | entradas nuevas {sum(r['decision'] == 'OPENED' for r in real)} "
                f"| rechazos {rejections} | decididas desde el celular: autorizadas {ev('ACCEPTED')}, "
                f"rechazadas {ev('REJECTED')}, vencidas {ev('EXPIRED')}",
                f"Posiciones abiertas {len(book.open)} en {len(pairs)} pares | cierres "
                f"{sum(r.get('action') == 'SETTLE' for r in trades)}",
                f"Caja US${book.cash:.2f} | capital bloqueado US${book.locked:.2f} | "
                f"P&L realizado US${book.realized_net:+.2f} | neto esperado abierto (no realizado) "
                f"US${expected:+.2f}"]
    return [f"Ciclos {len(cycles)} ({failed} fallidos) | oport. {len(opps)} | "
            f"net+ {netpos} | ejec. {exe}",
            f"Caja US${book.cash:.2f} (bloq. US${book.locked:.2f}) | "
            f"neto US${book.realized_net:+.2f}"]


def _funding_daily_lines(reports_dir):
    live = load_json(Path(reports_dir) / "live_summary.json", {}) or {}
    p0 = load_json(Path(reports_dir) / "phase0_summary.json", {}) or {}
    if not live and not p0:
        return ["sin datos todavía (corre en la PC local)"]
    lines = []
    if p0:
        t = p0.get("totals", {})
        lines.append(f"Fase 0 ({str(p0.get('generated_at'))[:10]}): oport. "
                     f"{t.get('ex_ante_positive', 0)} | net+ {t.get('net_positive_trades', 0)}"
                     f" | ejec. {t.get('executable_trades_100usd', 0)}")
    if live:
        pp = live.get("paper", {})
        lines.append(f"Vivo ({str(live.get('generated_at'))[:16]}): oport. "
                     f"{live.get('opportunities', 0)} | errores {live.get('errors', 0)} | "
                     f"caja US${pp.get('cash', 0):.2f} | neto US${pp.get('realized_net', 0):+.2f}")
    return lines


def compose_daily_message(data_dir, reports_dir="reports/funding_basis", now=None,
                          starting_cash=None):
    now = now or datetime.now(timezone.utc)
    since = now - timedelta(hours=24)
    starting_cash = (BotConfig().starting_capital_usd if starting_cash is None
                     else starting_cash)
    _, cur_body, _, _ = build_daily_message(data_dir, now, starting_cash)
    parts = ["[KALSHI_CURRENT]\n" + cur_body]
    for name, tag in STRATEGY_TAGS.items():
        parts.append(f"[{tag}]\n" + "\n".join(_strategy_daily_lines(
            Path(data_dir) / "strategies" / name, since, starting_cash)))
    parts.append("[FUNDING_BASIS]\n" + "\n".join(_funding_daily_lines(reports_dir)))
    lab = _lab_daily_lines(Path(reports_dir).parent / "lab" / "lab_summary.json")
    if lab:
        parts.append("[LAB]\n" + "\n".join(lab))
    return "Pie a pie: resumen diario", "\n\n".join(parts), 2, ["bar_chart"]


def _lab_daily_lines(path):
    """Resumen consolidado del laboratorio (último reporte generado en la PC)."""
    d = load_json(path, {}) or {}
    if not d:
        return []
    c = d.get("consolidated", {})
    run = d.get("run", {})
    lines = [f"Corrida {run.get('run_id', 'n/d')} ({str(run.get('started'))[:16]})"]
    for name, m in (d.get("strategies") or {}).items():
        ev = m.get("evidence", {})
        lines.append(f"{name}: ejec {ev.get('simulated_executed', 0)} | rent "
                     f"{ev.get('simulated_profitable', 0)} | {m.get('verdict', {}).get('label')}")
    lines.append(f"Consolidado: neto sim US${c.get('net_simulated_usd', 0):+.2f}")
    return lines


def authz_notifications(data_dir, since, env=os.environ):
    """Una notificación por solicitud nueva, con sus botones Autorizar / Rechazar si hay
    clave de firma. Sin clave sale igual, con la instrucción manual."""
    from . import authz
    key, topic = env.get(authz.KEY_ENV, "").strip(), authz.reply_topic(env)
    out = []
    for name, tag in STRATEGY_TAGS.items():
        d = Path(data_dir) / "strategies" / name
        decs = {r["request_id"]: r for r in read_csv(d / "decisions.csv") if r.get("new_request") == "1"}
        for q in rows_since(read_csv(d / "authorization_requests.csv"), since):
            buttons = bool(key and topic)
            actions = (authz.action_buttons(key, name, q["request_id"], q["timestamp"], topic)
                       if buttons else None)
            body = "\n".join(_auth_request_lines(q, decs.get(q["request_id"], {}), buttons))
            out.append((f"[{tag}] Autorización requerida", body, 4, ["raised_hand"], actions))
    return out


def send(topic, title, body, priority=3, tags=(), click=None, timeout=10, actions=None):
    """Publica en ntfy. Nunca levanta excepción: devuelve True/False."""
    if not topic:
        print("NTFY_TOPIC no definido: no se notifica.")
        return False
    payload = {"topic": topic, "title": title, "message": body,
               "priority": priority, "tags": list(tags)}
    if click:
        payload["click"] = click
    if actions:
        payload["actions"] = actions
    try:
        r = requests.post(NTFY_URL, json=payload, timeout=timeout)
        r.raise_for_status()
    except requests.RequestException as e:
        # No se imprime la URL ni el payload: contienen el topic.
        print(f"No se pudo notificar ({type(e).__name__}).")
        return False
    print("Notificación enviada.")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kind", choices=["cycle", "daily", "test"])
    p.add_argument("--since", help="inicio de la corrida (ISO, UTC); para 'cycle'")
    p.add_argument("--data", default=str(DATA))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    extra = []
    if args.kind == "cycle":
        since = _ts(args.since or "") or datetime.now(timezone.utc) - timedelta(minutes=20)
        msg = compose_cycle_message(args.data, since,
                                    os.environ.get("JOB_STATUS", "success"),
                                    os.environ.get("STEP_OUTCOMES", ""), authz_separate=True)
        extra = authz_notifications(args.data, since)
    elif args.kind == "daily":
        msg = compose_daily_message(args.data)
    else:
        msg = ("Pie a pie: prueba", "Si ves esto, las notificaciones andan.",
               3, ["white_check_mark"])

    topic = os.environ.get("NTFY_TOPIC", "").strip()
    msgs = ([(*msg, None)] if msg else []) + extra
    if not msgs:
        print("Nada que notificar.")
        return 0
    for title, body, priority, tags, actions in msgs:
        if args.dry_run:
            print(f"[{title}]\n{body}" + (f"\n(acciones: {[a['label'] for a in actions]})" if actions else ""))
        else:
            send(topic, title, body, priority, tags, click=os.environ.get("RUN_URL") or None,
                 actions=actions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
