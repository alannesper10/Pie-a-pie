"""Resúmenes de funding/basis. Lo que va a git es SOLO esto (reports/), nunca
la base SQLite de alta frecuencia."""

import json
from datetime import datetime
from pathlib import Path
from statistics import mean, median

REPORT_DIR = Path("reports") / "funding_basis"


def _write(name, data):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / name).write_text(json.dumps(data, indent=1, default=str,
                                              ensure_ascii=False), encoding="utf-8")


def phase0_summary(results, cfg, generated_at):
    pairs = []
    for r in results:
        bt = r.get("backtest", {})
        pairs.append({
            "exchange": r["exchange"], "asset": r["asset"], "status": r.get("status"),
            "errors": r.get("errors", []), "coverage_days": r.get("coverage_days"),
            "rows": r.get("rows"), "funding_interval_h": r.get("funding_interval_h"),
            "funding_stats": r.get("funding_stats"), "basis_stats": r.get("basis_stats"),
            "round_trip_cost_pct": r.get("round_trip_cost_pct"),
            "leg_fail_expected_cost_pct": r.get("leg_fail_expected_cost_pct"),
            "breakeven_periods_at_mean_rate": r.get("breakeven_periods_at_mean_rate"),
            "costs": r.get("costs"), "book_now": r.get("book_now"),
            "feasibility_100usd": r.get("feasibility_100usd"), "backtest": bt,
            "sensitivity_by_horizon_days": r.get("sensitivity_by_horizon_days"),
        })
    ok = [p for p in pairs if p["status"] == "OK"]
    totals = {
        "pairs": len(pairs), "pairs_ok": len(ok),
        "decisions": sum(p["backtest"].get("decisions", 0) for p in ok),
        "ex_ante_positive": sum(p["backtest"].get("ex_ante_positive", 0) for p in ok),
        "trades": sum(p["backtest"].get("trades", 0) for p in ok),
        "net_positive_trades": sum(p["backtest"].get("net_positive_trades", 0) for p in ok),
        "executable_trades_100usd": sum(p["backtest"].get("executable_trades_100usd", 0)
                                        for p in ok),
        "net_usd_total_all_pairs": sum(p["backtest"].get("net_usd_total", 0.0) for p in ok),
        "feasible_pairs_100usd": sum(bool((p["feasibility_100usd"] or {}).get("feasible"))
                                     for p in ok),
    }
    data = {"generated_at": generated_at, "strategy": "funding_basis", "phase": 0,
            "paper_only": True, "history_days": cfg.history_days,
            "rule": {"horizon_days": cfg.horizon_days, "trailing_periods": cfg.trailing_periods,
                     "max_hold_days": cfg.max_hold_days, "leverage": cfg.leverage,
                     "capital_usd": cfg.starting_capital_usd, "allocation": cfg.allocation},
            "totals": totals, "pairs": pairs}
    _write("phase0_summary.json", data)
    _write_markdown(data)
    return data


def _pct(x, d=3):
    return "n/d" if x is None else f"{100 * x:.{d}f}%"


def _write_markdown(d):
    t = d["totals"]
    lines = [
        "# Funding/basis — Fase 0 (histórico)", "",
        f"Generado: {d['generated_at']} · {d['history_days']} días · paper only · "
        f"spot largo + perp corto, mismo exchange, {d['rule']['leverage']:g}x", "",
        f"**Pares analizados:** {t['pairs_ok']}/{t['pairs']} · **decisiones:** {t['decisions']} · "
        f"**oportunidades ex-ante:** {t['ex_ante_positive']} · **trades:** {t['trades']} · "
        f"**net-positive:** {t['net_positive_trades']} · **ejecutables con US$100:** "
        f"{t['executable_trades_100usd']} · **pares factibles con US$100:** "
        f"{t['feasible_pairs_100usd']}", "",
        "| Exchange | Activo | Funding medio | Intervalo | % positivo | Costo ida+vuelta "
        "| Breakeven (períodos) | Trades | Net+ | Neto US$ | Factible US$100 | Capital mínimo |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in d["pairs"]:
        fs, bt, fe = p.get("funding_stats") or {}, p.get("backtest") or {}, p.get("feasibility_100usd") or {}
        be = p.get("breakeven_periods_at_mean_rate")
        lines.append(
            f"| {p['exchange']} | {p['asset']} | {_pct(fs.get('mean'), 4)} | "
            f"{(p.get('funding_interval_h') or {}).get('inferred_from_history', 'n/d')}h | "
            f"{_pct(fs.get('pct_positive'), 0)} | {_pct(p.get('round_trip_cost_pct'))} | "
            f"{'n/d' if be is None else f'{be:.0f}'} | {bt.get('trades', 0)} | "
            f"{bt.get('net_positive_trades', 0)} | {bt.get('net_usd_total', 0):+.3f} | "
            f"{fe.get('feasible')} | {fe.get('min_capital_usd', 'n/d')} |")
    lines += ["", "## Sensibilidad al horizonte de decisión (misma regla, mismos datos)", "",
              "No reemplaza el resultado base (7 días). Muestra qué horizonte haría falta "
              "para que haya entradas y si terminaron en neto positivo.", "",
              "| Exchange | Activo | Horizonte | Oport. ex-ante | Trades | Net+ | Neto US$ "
              "| Funding US$ | Basis US$ | Costos US$ |", "|---|---|---|---|---|---|---|---|---|---|"]
    for p in d["pairs"]:
        for h, r in (p.get("sensitivity_by_horizon_days") or {}).items():
            lines.append(f"| {p['exchange']} | {p['asset']} | {h} d | {r['ex_ante_positive']} | "
                         f"{r['trades']} | {r['net_positive_trades']} | {r['net_usd_total']:+.3f} | "
                         f"{r['funding_usd_total']:+.3f} | {r['basis_pnl_usd_total']:+.3f} | "
                         f"{r['costs_usd_total']:.3f} |")
    errs = [(p["exchange"], p["asset"], e) for p in d["pairs"] for e in p.get("errors", [])]
    lines += ["", "## Errores de datos", ""]
    lines += [f"- {a} {b}: {e}" for a, b, e in errs] or ["- ninguno"]
    (REPORT_DIR / "phase0_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def live_summary(storage, ledger, generated_at):
    opps = storage.db.execute(
        "SELECT exchange, asset, opened_at, closed_at, snapshots, max_expected_net_pct, "
        "max_size_usd FROM opportunities").fetchall()
    closed = [o for o in opps if o[3]]
    mins = [(datetime.fromisoformat(o[3]) - datetime.fromisoformat(o[2])).total_seconds() / 60
            for o in closed]
    data = {
        "generated_at": generated_at, "strategy": "funding_basis", "phase": 1,
        "paper_only": True,
        "snapshots": storage.count("snapshots"),
        "opportunities": len(opps), "opportunities_open": len(opps) - len(closed),
        "opportunities_feasible": sum(1 for o in opps if (o[6] or 0) > 0),
        "duration_minutes": {"mean": mean(mins) if mins else None,
                             "median": median(mins) if mins else None,
                             "n_closed": len(mins)},
        "max_expected_net_pct": max((o[5] for o in opps), default=None),
        "errors": storage.count("errors"),
        "errors_by_exchange": dict(storage.db.execute(
            "SELECT exchange, COUNT(*) FROM errors GROUP BY exchange").fetchall()),
        "paper": {"cash": ledger.cash, "locked": ledger.locked,
                  "open_positions": len(ledger.open), "closed_positions": len(ledger.closed),
                  "net_positive_closed": sum((p.realized_net or 0) > 0 for p in ledger.closed),
                  "failed_entries": ledger.failed_entries,
                  "failed_entry_costs": ledger.failed_entry_costs,
                  "realized_net": ledger.realized_net,
                  "fees": sum(p.entry_fees + p.exit_fees for p in ledger.closed)
                  + sum(p.entry_fees for p in ledger.open)},
        "events": dict(storage.db.execute(
            "SELECT event, COUNT(*) FROM paper_events GROUP BY event").fetchall()),
    }
    _write("live_summary.json", data)
    return data


def ntfy_text(live):
    p = live["paper"]
    return ("[FUNDING_BASIS] Pie a pie: resumen",
            "\n".join([
                f"Snapshots: {live['snapshots']} | errores: {live['errors']}",
                f"Oportunidades: {live['opportunities']} (factibles {live['opportunities_feasible']})",
                f"Paper: {p['open_positions']} abiertas, {p['closed_positions']} cerradas",
                f"Caja: US${p['cash']:.2f} (bloqueado US${p['locked']:.2f})",
                f"Neto realizado: US${p['realized_net']:+.2f}",
            ]))
