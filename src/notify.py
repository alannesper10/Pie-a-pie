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
        msg = build_cycle_message(args.data, since,
                                  os.environ.get("JOB_STATUS", "success"),
                                  os.environ.get("STEP_OUTCOMES", ""))
    elif args.kind == "daily":
        msg = build_daily_message(args.data)
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
