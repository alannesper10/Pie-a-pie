"""Comparación de estrategias. Cada una se lee de SU propia fuente; nunca se
suman capitales ni P&L entre estrategias. Si una da cero, muestra cero.

  python -m src.compare            imprime la tabla
  python -m src.compare --write    además escribe reports/strategy_comparison.{md,json}
"""

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median

from .paper_trader import PaperBook
from .tracking import load_json, read_csv

STRATEGIES = ["kalshi_current", "buy_all_no", "strike_inconsistency", "funding_basis"]


def _f(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _stats(values):
    return {"n": len(values), "mean": mean(values) if values else None,
            "median": median(values) if values else None,
            "max": max(values) if values else None}


def _book_metrics(state_path, starting, trades):
    book = PaperBook.from_dict((load_json(state_path, {}) or {}).get("paper"), starting)
    opened = [t for t in trades if t.get("action") == "OPEN"]
    return {"cash": book.cash, "locked": book.locked, "open_positions": len(book.open),
            "closed_positions": len(book.closed), "pnl_realized": book.realized_net,
            "paper_fees": sum(_f(t.get("fees")) for t in opened),
            "paper_slippage": sum(_f(t.get("slippage")) for t in opened)}


def kalshi_current(data_dir, starting=100.0):
    d = Path(data_dir)
    cycles = read_csv(d / "cycles.csv")
    rows = read_csv(d / "near_misses.csv")
    durs = read_csv(d / "opportunity_durations.csv")
    exe = [r for r in rows if r.get("executable") == "True"]
    netpos = [r for r in rows if _f(r.get("est_net")) > 0 and _f(r.get("depth_with_edge")) >= 1
              and r.get("reason") != "SUSPICIOUS_EDGE_CHECK_RULES"]
    reasons = Counter(r["reason"] for r in rows if r.get("executable") != "True")
    ok = [c for c in cycles if c.get("ok") == "1"]
    return {
        "strategy": "kalshi_current", "source": str(d),
        "cycles": len(cycles), "cycles_ok": len(ok),
        "opportunities": len(rows), "net_positive": len(netpos), "executable": len(exe),
        "discarded": sum(reasons.values()),
        "discard_reasons": dict(reasons.most_common()),
        "discard_note": ("los descartes del prefiltro de kalshi_current no se registran "
                         "(no se modificó su código); solo se cuentan los evaluados"),
        "duration_cycles": _stats([_f(r["cycles"]) for r in durs]),
        "duration_minutes": _stats([_f(r["minutes"]) for r in durs]),
        "capital_per_bundle": _stats([_f(r["ask_sum"]) for r in rows]),
        "fees_per_opportunity": _stats([_f(r["est_fees"]) for r in rows]),
        "size_available": _stats([_f(r["depth_with_edge"]) for r in rows]),
        "opportunities_per_cycle": len(rows) / len(ok) if ok else 0.0,
        **_book_metrics(d / "state.json", starting, read_csv(d / "paper_trades.csv")),
    }


def kalshi_strategy(name, root, starting=100.0):
    d = Path(root) / name
    cycles = read_csv(d / "cycles.csv")
    rows = read_csv(d / "opportunities.csv")
    durs = read_csv(d / "durations.csv")
    disc = read_csv(d / "discards.csv")
    reasons = Counter()
    for r in disc:
        reasons[r["reason"]] += int(_f(r["count"]))
    exe = [r for r in rows if r.get("executable") == "True"]
    netpos = [r for r in rows if _f(r.get("net_profit")) > 0
              and _f(r.get("max_contracts_available")) >= 1
              and r.get("reason") != "SUSPICIOUS_EDGE_CHECK_RULES"]
    ok = [c for c in cycles if c.get("ok") == "1"]
    outlays = [_f(x.split("=", 1)[1]) for r in rows for x in r.get("detail", "").split(";")
               if x.startswith("min_bundle_outlay=")]
    return {
        "strategy": name, "source": str(d),
        "cycles": len(cycles), "cycles_ok": len(ok),
        "opportunities": len(rows), "net_positive": len(netpos), "executable": len(exe),
        "discarded": sum(reasons.values()), "discard_reasons": dict(reasons.most_common()),
        "duration_cycles": _stats([_f(r["cycles"]) for r in durs]),
        "duration_minutes": _stats([_f(r["minutes"]) for r in durs]),
        "capital_per_bundle": _stats(outlays),
        "fees_per_opportunity": _stats([_f(r["fees"]) for r in rows]),
        "size_available": _stats([_f(r["max_contracts_available"]) for r in rows]),
        "opportunities_per_cycle": len(rows) / len(ok) if ok else 0.0,
        **_book_metrics(d / "state.json", starting, read_csv(d / "paper_trades.csv")),
    }


def funding_basis(reports_dir, starting=100.0):
    d = Path(reports_dir)
    p0 = load_json(d / "phase0_summary.json", {}) or {}
    live = load_json(d / "live_summary.json", {}) or {}
    t = p0.get("totals", {})
    paper = live.get("paper", {})
    pairs = p0.get("pairs", [])
    costs = [p["round_trip_cost_pct"] for p in pairs if p.get("round_trip_cost_pct") is not None]
    mins = [(p.get("feasibility_100usd") or {}).get("min_capital_usd") for p in pairs]
    return {
        "strategy": "funding_basis", "source": str(d),
        "phase0_generated_at": p0.get("generated_at"),
        "phase0_pairs_ok": t.get("pairs_ok", 0), "phase0_decisions": t.get("decisions", 0),
        "cycles": live.get("snapshots", 0), "cycles_note": "snapshots en vivo (par x tick)",
        "opportunities": t.get("ex_ante_positive", 0) + live.get("opportunities", 0),
        "net_positive": t.get("net_positive_trades", 0) + paper.get("net_positive_closed", 0),
        "executable": t.get("executable_trades_100usd", 0) + paper.get("open_positions", 0)
        + paper.get("closed_positions", 0),
        "discarded": t.get("decisions", 0) - t.get("ex_ante_positive", 0),
        "discard_reasons": {"COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO":
                            t.get("decisions", 0) - t.get("ex_ante_positive", 0),
                            "INFEASIBLE_MIN_SIZE_100USD_PAIRS":
                            t.get("pairs_ok", 0) - t.get("feasible_pairs_100usd", 0)},
        "duration_minutes": live.get("duration_minutes", {}),
        "capital_per_bundle": _stats([m for m in mins if m is not None]),
        "fees_per_opportunity": _stats(costs),
        "fees_note": "costo ida+vuelta como fracción del nocional",
        "size_available": {"n": None},
        "cash": paper.get("cash", starting), "locked": paper.get("locked", 0.0),
        "open_positions": paper.get("open_positions", 0),
        "closed_positions": paper.get("closed_positions", 0),
        "pnl_realized": paper.get("realized_net", 0.0),
        "paper_fees": paper.get("fees", 0.0), "paper_slippage": None,
        "phase0_net_usd_total": t.get("net_usd_total_all_pairs", 0.0),
        "live_errors": live.get("errors"),
    }


def build(data_dir="data", reports_dir="reports/funding_basis"):
    root = Path(data_dir) / "strategies"
    return {"kalshi_current": kalshi_current(data_dir),
            "buy_all_no": kalshi_strategy("buy_all_no", root),
            "strike_inconsistency": kalshi_strategy("strike_inconsistency", root),
            "funding_basis": funding_basis(reports_dir)}


def _fmt(v):
    if v is None:
        return "n/d"
    if isinstance(v, float):
        return f"{v:.4g}" if abs(v) < 1000 else f"{v:,.0f}"
    return str(v)


def render(cmp):
    rows = [
        ("Ciclos (ok)", lambda m: f"{m['cycles']}" + (f" ({m['cycles_ok']})" if "cycles_ok" in m else "")),
        ("Oportunidades", lambda m: m["opportunities"]),
        ("Net-positive", lambda m: m["net_positive"]),
        ("Ejecutables", lambda m: m["executable"]),
        ("Descartadas", lambda m: m["discarded"]),
        ("Duración media (min)", lambda m: (m.get("duration_minutes") or {}).get("mean")),
        ("Capital por paquete (media)", lambda m: (m.get("capital_per_bundle") or {}).get("mean")),
        ("Fees por oportunidad (media)", lambda m: (m.get("fees_per_opportunity") or {}).get("mean")),
        ("Tamaño disponible (máx)", lambda m: (m.get("size_available") or {}).get("max")),
        ("Oport. por ciclo", lambda m: m.get("opportunities_per_cycle")),
        ("Caja paper US$", lambda m: m["cash"]),
        ("Capital bloqueado US$", lambda m: m["locked"]),
        ("Fees paper US$", lambda m: m.get("paper_fees")),
        ("Slippage paper US$", lambda m: m.get("paper_slippage")),
        ("P&L realizado US$", lambda m: m["pnl_realized"]),
    ]
    head = "| Métrica | " + " | ".join(STRATEGIES) + " |"
    out = [head, "|" + "---|" * (len(STRATEGIES) + 1)]
    for label, fn in rows:
        out.append(f"| {label} | " + " | ".join(_fmt(fn(cmp[s])) for s in STRATEGIES) + " |")
    out += ["", "Motivos de descarte (top 5 por estrategia):"]
    for s in STRATEGIES:
        top = list(cmp[s]["discard_reasons"].items())[:5]
        out.append(f"- {s}: " + (", ".join(f"{k}={v}" for k, v in top) or "ninguno"))
    out.append(f"- nota kalshi_current: {cmp['kalshi_current']['discard_note']}")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    p.add_argument("--data", default="data")
    p.add_argument("--reports", default="reports/funding_basis")
    args = p.parse_args(argv)
    cmp = build(args.data, args.reports)
    text = render(cmp)
    print(text)
    if args.write:
        out = Path("reports")
        out.mkdir(exist_ok=True)
        (out / "strategy_comparison.md").write_text(
            "# Comparación de estrategias (paper only)\n\n" + text + "\n", encoding="utf-8")
        (out / "strategy_comparison.json").write_text(
            json.dumps(cmp, indent=1, default=str, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
