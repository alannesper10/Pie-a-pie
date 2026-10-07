"""Resumen de lo registrado por el modo continuo (--report)."""

from pathlib import Path
from statistics import mean, median

from .paper_trader import PaperBook
from .tracking import load_json, read_csv


def _stats(values):
    if not values:
        return "n/d"
    return f"promedio {mean(values):.1f} | mediana {median(values):.1f}"


def build_report(data_dir, starting_cash, interval_min):
    d = Path(data_dir)
    cycles = read_csv(d / "cycles.csv")
    near = read_csv(d / "near_misses.csv")
    durations = read_csv(d / "opportunity_durations.csv")
    state = load_json(d / "state.json", {}) or {}
    book = PaperBook.from_dict(state.get("paper"), starting_cash)
    active = state.get("streaks", {})

    ok = sum(c["ok"] == "1" for c in cycles)
    exe_rows = [r for r in near if r["executable"] == "True"]
    cyc = [int(r["cycles"]) for r in durations]
    mins = [float(r["minutes"]) for r in durations]
    ends = {}
    for r in durations:
        ends[r["end_reason"]] = ends.get(r["end_reason"], 0) + 1

    lines = [
        "=" * 70,
        "REPORTE PAPER TRADING",
        "=" * 70,
        f"Ciclos: {len(cycles)} ({ok} ok, {len(cycles) - ok} fallidos)"
        + (f" | {cycles[0]['timestamp'][:16]} -> {cycles[-1]['timestamp'][:16]}"
           if cycles else ""),
        f"Casi-aciertos (suma ask < 1,03): {len(near)} registros, "
        f"{len({r['event_ticker'] for r in near})} eventos distintos",
        f"Ejecutables: {len(exe_rows)} registros, "
        f"{len({r['event_ticker'] for r in exe_rows})} eventos distintos",
        "",
        f"Duración de oportunidades ({len(durations)} rachas cerradas, "
        f"{len(active)} abiertas):",
        f"  ciclos seguidos:            {_stats(cyc)}",
        f"  minutos (primer-último):    {_stats(mins)}",
        f"  resolución: {interval_min:g} min; una racha de 1 ciclo dura entre "
        f"0 y ~{interval_min:g} min",
    ]
    if ends:
        lines.append("  fin de racha: " + ", ".join(
            f"{k}={v}" for k, v in sorted(ends.items())))
    lines += [
        "",
        "Paper:",
        f"  caja libre:          US${book.cash:.2f}",
        f"  capital bloqueado:   US${book.locked:.2f} en {len(book.open)} "
        "posiciones abiertas",
        f"  neto esperado abierto: US${sum(p.expected_net for p in book.open):+.2f}",
        f"  posiciones cerradas: {len(book.closed)}",
        f"  NETO TOTAL REALIZADO: US${book.realized_net:+.2f}",
    ]
    for p in book.open:
        lines.append(f"    abierta {p.event_ticker}: {p.contracts} contratos, "
                     f"US${p.outlay:.2f} bloqueados, cierre esperado "
                     f"{p.expected_close or 'n/d'}")
    return "\n".join(lines)
