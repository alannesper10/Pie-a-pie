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


def build_strategy_cycle_lines(strategy_dir, since, step_failed=False):
    """Líneas importantes de UNA estrategia en esta corrida, o [] si no hay nada.

    Importante = ejecutable, paper abierta/cerrada o error. Los casi-aciertos
    y los net-positive no ejecutables van al resumen diario, no acá.
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
    for r in opps:
        if r.get("executable") == "True":
            lines.append(f"Ejecutable: {r['key'][:60]}, {r['contracts']} contratos, "
                         f"neto {_money(r['net_profit'])}")
    for r in trades:
        if r.get("action") == "OPEN":
            lines.append(f"Paper abierta: {r['event_ticker']}, neto esp. "
                         f"{_money(r['expected_net'])}")
        elif r.get("action") == "SETTLE":
            lines.append(f"Paper cerrada: {r['event_ticker']}, neto "
                         f"{_money(r['realized_net'])}")
    if trades:
        lines.append(f"Caja: US${float(trades[-1]['cash_after']):.2f}")
    return lines


def compose_cycle_message(data_dir, since, job_status="success", outcomes=""):
    """Una sola notificación por corrida con una sección por estrategia."""
    sections, priority = [], 0
    cur = build_cycle_message(data_dir, since, job_status, outcomes)
    if cur:
        sections.append(("KALSHI_CURRENT", cur[0].replace("Pie a pie: ", ""), cur[1]))
        priority = max(priority, cur[2])
    step_failed = "strategies" in failed_steps(outcomes)
    for name, tag in STRATEGY_TAGS.items():
        lines = build_strategy_cycle_lines(Path(data_dir) / "strategies" / name,
                                           since, step_failed)
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
    return "Pie a pie: resumen diario", "\n\n".join(parts), 2, ["bar_chart"]


def send(topic, title, body, priority=3, tags=(), click=None, timeout=10):
    """Publica en ntfy. Nunca levanta excepción: devuelve True/False."""
    if not topic:
        print("NTFY_TOPIC no definido: no se notifica.")
        return False
    payload = {"topic": topic, "title": title, "message": body,
               "priority": priority, "tags": list(tags)}
    if click:
        payload["click"] = click
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

    if args.kind == "cycle":
        since = _ts(args.since or "") or datetime.now(timezone.utc) - timedelta(minutes=20)
        msg = compose_cycle_message(args.data, since,
                                    os.environ.get("JOB_STATUS", "success"),
                                    os.environ.get("STEP_OUTCOMES", ""))
    elif args.kind == "daily":
        msg = compose_daily_message(args.data)
    else:
        msg = ("Pie a pie: prueba", "Si ves esto, las notificaciones andan.",
               3, ["white_check_mark"])

    if msg is None:
        print("Nada que notificar.")
        return 0
    title, body, priority, tags = msg
    if args.dry_run:
        print(f"[{title}]\n{body}")
        return 0
    send(os.environ.get("NTFY_TOPIC", "").strip(), title, body, priority, tags,
         click=os.environ.get("RUN_URL") or None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
