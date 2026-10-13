"""Evaluación y reporte del laboratorio. No maquilla: cero es cero, y una
estrategia solo se declara RENTABLE con resultados netos simulados,
ejecutables y evidencia mínima (cantidad, períodos, fuera de muestra, estrés).
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median, pstdev

REPORT_DIR = Path("reports") / "lab"

CATEGORIES = {
    "1. Entre exchanges (cripto)": ["cross_exchange"],
    "2. Basis spot-futuros / funding": ["basis_funding"],
    "3. Triangular": ["triangular"],
    "4. Mercados de predicción": ["polymarket_buy_all_no", "prediction_cross_venue"],
    "5. Provisión de liquidez": ["liquidity_provision"],
}
MIN_TRADES = 30
MIN_PERIODS = 6
MIN_POSITIVE_PERIODS = 0.6
OOS_THRESHOLDS = (0.0, 0.0005, 0.001, 0.002, 0.005)


def _sim_net(r):
    s = r.get("sim") or {}
    return s.get("net_usd")


def _pctiles(xs):
    if not xs:
        return None
    s = sorted(xs)
    q = lambda p: s[min(len(s) - 1, int(round(p * (len(s) - 1))))]  # noqa: E731
    return {"p5": q(0.05), "p25": q(0.25), "p50": q(0.5), "p75": q(0.75), "p95": q(0.95),
            "mean": mean(s), "std": pstdev(s) if len(s) > 1 else 0.0, "n": len(s)}


def _cost_sum(r):
    return sum((c or {}).get("usd", 0.0) for c in (r.get("costs") or {}).values())


def durations(rows):
    """Rachas de ticks consecutivos con neto estimado > 0 por clave."""
    by_key = defaultdict(list)
    for r in rows:
        if r.get("net_estimated_usd", 0) > 0:
            by_key[r["key"]].append(r["tick"])
    runs = []
    for ticks in by_key.values():
        ticks = sorted(set(ticks))
        start = prev = ticks[0]
        for t in ticks[1:]:
            if t != prev + 1:
                runs.append(prev - start + 1)
                start = t
            prev = t
        runs.append(prev - start + 1)
    return runs


def out_of_sample(rows):
    """Elige el umbral de neto estimado con la 1a mitad (cronológica) y lo
    evalúa en la 2a. Solo filas ejecutadas con neto simulado."""
    ex = [r for r in rows if r.get("decision") == "ACCEPTED" and _sim_net(r) is not None]
    ticks = sorted({r["tick"] for r in rows})
    if len(ticks) < 2:
        return {"status": "INSUFICIENTES_TICKS"}
    cut = ticks[len(ticks) // 2]
    ins = [r for r in ex if r["tick"] < cut]
    oos = [r for r in ex if r["tick"] >= cut]
    score = lambda rs, th: sum(_sim_net(r) for r in rs if r.get("net_estimated_pct", 0) >= th)  # noqa: E731
    best = max(OOS_THRESHOLDS, key=lambda th: (score(ins, th), -th))
    return {"split_tick": cut, "threshold": best, "in_sample_trades": len(ins),
            "in_sample_net": score(ins, best),
            "out_of_sample_trades": sum(r.get("net_estimated_pct", 0) >= best for r in oos),
            "out_of_sample_net": score(oos, best)}


NATURE = {"basis_funding": "statistical", "liquidity_provision": "statistical",
          "prediction_cross_venue": "unverifiable", "stat_arb_pairs": "statistical",
          "etf_relations": "statistical", "calendar_spread": "statistical",
          "orderbook_imbalance": "statistical"}
STATISTICAL_NATURES = ("statistical", "speculative")


def strategy_metrics(name, rows, ledger):
    # Para el veredicto de arbitraje solo cuentan las operaciones clasificadas
    # ARBITRAJE_GARANTIZADO; el resto se reporta pero no suma "rentabilidad".
    by_class = Counter(r.get("classification") or "SIN_CLASIFICAR" for r in rows)
    nature = NATURE.get(name, "arbitrage")
    accepted = [r for r in rows if r.get("decision") == "ACCEPTED"]
    if nature in STATISTICAL_NATURES:
        # Estrategia estadística: se cuentan TODAS las operaciones ejecutadas
        # (ganadoras y perdedoras). Contar solo las clasificadas positivas sería
        # sesgo de selección (bug detectado en la consolidación).
        sims = accepted
    else:
        sims = [r for r in accepted if r.get("classification") == "ARBITRAJE_GARANTIZADO"]
    nets = [_sim_net(r) for r in sims if _sim_net(r) is not None]
    pcts = [(r.get("sim") or {}).get("net_pct_capital") for r in sims
            if (r.get("sim") or {}).get("net_pct_capital") is not None]
    realized = [r for r in sims if (r.get("sim") or {}).get("realized", True)]
    cap = sum(r.get("capital_usd", 0) for r in sims if _sim_net(r) is not None)
    periods = defaultdict(float)
    for r in sims:
        if _sim_net(r) is not None:
            periods[r["ts"][:15]] += _sim_net(r)      # períodos de 10 minutos
    pv = list(periods.values())
    stress = {}
    for k in (1.5, 2.0):
        stress[str(k)] = {
            "estimated_positive": sum(1 for r in rows
                                      if r.get("gross_usd", 0) - k * _cost_sum(r) > 0),
            "simulated_net": sum(_sim_net(r) - (k - 1) * _cost_sum(r) for r in sims
                                 if _sim_net(r) is not None)}
    durs = durations(rows)
    m = {
        "strategy": name,
        "evidence": {
            "observed": len(rows),
            "estimated_positive": sum(r.get("net_estimated_usd", 0) > 0 for r in rows),
            "simulated_executed": len(sims),
            "simulated_profitable": sum(n > 0 for n in nets),
            "realized_trades": len(realized),
            "not_realized_trades": len(sims) - len(realized),
        },
        "reasons": dict(Counter(r.get("reason") for r in rows).most_common(12)),
        "classification": dict(by_class), "nature": nature,
        "accepted_not_counted": len(accepted) - len(sims),
        "by_category": category_breakdown(rows),
        "by_market": market_breakdown(sims),
        "sensitivity": sensitivity(sims),
        "net_simulated_usd": sum(nets),
        "capital_committed_usd": cap,
        "return_on_committed": sum(nets) / cap if cap else None,
        "losses": {"n": sum(n < 0 for n in nets), "usd": sum(n for n in nets if n < 0)},
        "distribution_net_pct": _pctiles(pcts),
        "duration_ticks": _pctiles(durs),
        "periods": {"n": len(pv), "positive_share": (sum(p > 0 for p in pv) / len(pv)) if pv else None,
                    "std": pstdev(pv) if len(pv) > 1 else None, "values": pv},
        "stress": stress,
        "out_of_sample": out_of_sample(rows),
        "ledger": ledger,
    }
    m["verdict"] = verdict(m)
    if nature in STATISTICAL_NATURES:
        m["verdict"] = {"label": f"ESTADISTICA: {m['verdict']['label']} (no es arbitraje)",
                        "why": f"neto simulado {m['net_simulated_usd']:+.4f} USD; "
                               + m["verdict"]["why"]}
    elif nature == "unverifiable":
        m["verdict"] = {"label": "NO VERIFICABLE", "why": "sin pares verificados a mano"}
    return m


def category_breakdown(rows):
    """Conteos y sumas SEPARADOS por categoría: nunca se mezclan en un total."""
    out = {}
    for r in rows:
        c = r.get("classification") or "SIN_CLASIFICAR"
        d = out.setdefault(c, {"n": 0, "net_estimated_usd": 0.0, "net_simulated_usd": 0.0,
                               "capital_usd": 0.0, "max_loss_usd": 0.0})
        d["n"] += 1
        d["net_estimated_usd"] += r.get("net_estimated_usd") or 0.0
        d["net_simulated_usd"] += _sim_net(r) or 0.0
        d["capital_usd"] += r.get("capital_usd") or 0.0
        d["max_loss_usd"] = max(d["max_loss_usd"], r.get("max_loss_usd") or 0.0)
    return out


def market_breakdown(rows):
    out = defaultdict(lambda: {"n": 0, "net_usd": 0.0})
    for r in rows:
        k = "+".join(r.get("venues") or []) + ":" + "+".join(r.get("instruments") or [])[:60]
        out[k]["n"] += 1
        out[k]["net_usd"] += _sim_net(r) or 0.0
    return dict(out)


def sensitivity(rows):
    """Neto simulado ante costos más exigentes, separando comisiones y
    deslizamiento. La latencia se compara entre corridas con distinta latencia
    de recolección (no se puede inventar un libro a otra latencia)."""
    def scaled(fee_k, slip_k):
        tot = 0.0
        for r in rows:
            n = _sim_net(r)
            if n is None:
                continue
            extra = 0.0
            for name, c in (r.get("costs") or {}).items():
                k = slip_k if "slip" in name.lower() or "profundidad" in name.lower() else fee_k
                extra += (k - 1) * (c or {}).get("usd", 0.0)
            tot += n - extra
        return tot
    return {"fees_x1.5": scaled(1.5, 1.0), "fees_x2": scaled(2.0, 1.0),
            "slippage_x2": scaled(1.0, 2.0), "fees_x1.5_slippage_x2": scaled(1.5, 2.0)}


def verdict(m):
    ev, oos = m["evidence"], m["out_of_sample"]
    net = m["net_simulated_usd"]
    if ev["simulated_executed"] < MIN_TRADES or m["periods"]["n"] < MIN_PERIODS:
        why = (f"{ev['simulated_executed']} ejecuciones simuladas (mín {MIN_TRADES}), "
               f"{m['periods']['n']} períodos (mín {MIN_PERIODS})")
        tail = "; neto simulado negativo" if net < 0 else ""
        return {"label": "SIN EVIDENCIA SUFICIENTE", "why": why + tail}
    checks = {"neto > 0": net > 0,
              "fuera de muestra > 0": (oos.get("out_of_sample_net") or 0) > 0,
              "estrés x1.5 > 0": m["stress"]["1.5"]["simulated_net"] > 0,
              f"períodos positivos >= {MIN_POSITIVE_PERIODS:.0%}":
                  (m["periods"]["positive_share"] or 0) >= MIN_POSITIVE_PERIODS}
    if ev["not_realized_trades"]:
        checks["P&L realizado (no solo mínimo garantizado/abierto)"] = ev["realized_trades"] >= MIN_TRADES
    ok = all(checks.values())
    return {"label": "RENTABLE (evidencia mínima)" if ok else "NO RENTABLE",
            "why": ", ".join(f"{k}: {'sí' if v else 'no'}" for k, v in checks.items())}


def external_evidence():
    """Evidencia que NO se recalcula en el laboratorio: Kalshi (Actions, data/)
    y funding Fase 0 histórica. Solo lectura."""
    out = {}
    try:
        from src.compare import build
        c = build("data", "reports/funding_basis")
        for k in ("kalshi_current", "buy_all_no", "strike_inconsistency"):
            m = c[k]
            out[k] = {"source": "data/ (GitHub Actions, solo lectura)", "cycles": m["cycles"],
                      "opportunities": m["opportunities"], "net_positive": m["net_positive"],
                      "executable": m["executable"], "pnl_realized": m["pnl_realized"]}
        out["funding_phase0"] = {"source": "reports/funding_basis/phase0_summary.json",
                                 **c["funding_basis"]}
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def build_report(store, run_id):
    info = store.run_info(run_id) or {}
    ledgers = store.ledgers(run_id)
    names = sorted({*ledgers, *[s for s, *_ in store.tick_stats(run_id)]})
    per = {n: strategy_metrics(n, store.opportunities(run_id, n), ledgers.get(n)) for n in names}
    lab_names = [n for n in per]
    consolidated = {
        "strategies": len(lab_names),
        "capital_total_usd": sum((per[n]["ledger"] or {}).get("capital", 0) for n in lab_names),
        "net_simulated_usd": sum(per[n]["net_simulated_usd"] for n in lab_names),
        "realized_usd": sum((per[n]["ledger"] or {}).get("realized", 0) for n in lab_names),
        "executed": sum(per[n]["evidence"]["simulated_executed"] for n in lab_names),
        "profitable": sum(per[n]["evidence"]["simulated_profitable"] for n in lab_names),
        "note": "suma de estrategias con capital separado; la liquidez se reclamó una sola vez por tick",
    }
    errors = store.error_rows(run_id)
    err_by = Counter(f"{e.get('venue')}:{e.get('what')}" for e in errors)
    data = {"run": info, "ticks": store.tick_stats(run_id), "strategies": per,
            "consolidated": consolidated, "external": external_evidence(),
            "errors": {"total": len(errors), "by_source": dict(err_by.most_common(20))},
            "categories": CATEGORIES}
    return data


def _p(x, d=3):
    return "n/d" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.{d}f}%"


def _u(x):
    return "n/d" if x is None else f"US${x:+.4f}"


def render_markdown(d):
    run = d["run"]
    L = [f"# Laboratorio Pie a Pie — {run.get('run_id')}", "",
         f"Modo: {run.get('mode')} · inicio {run.get('started')} · semilla {run.get('seed')}"
         + (f" · replay de {run.get('source_run')}" if run.get("source_run") else ""), "",
         "Todo es SIMULADO. OBSERVADO = datos públicos crudos; ESTIMADO = neto con costos "
         "modelados; SIMULADO = ejecución con latencia, fills parciales y liquidez compartida.", "",
         "## Comparación por estrategia", "",
         "| Estrategia | Observadas | Estimadas > 0 | Ejecutadas (sim) | Rentables (sim) | "
         "Neto sim. | Capital comprometido | Retorno s/ capital | Peor/mejor (p5/p95) | Veredicto |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for n, m in d["strategies"].items():
        ev, dist = m["evidence"], m["distribution_net_pct"] or {}
        L.append(f"| {n} | {ev['observed']} | {ev['estimated_positive']} | {ev['simulated_executed']} | "
                 f"{ev['simulated_profitable']} | {_u(m['net_simulated_usd'])} | "
                 f"US${m['capital_committed_usd']:.2f} | {_p(m['return_on_committed'])} | "
                 f"{_p(dist.get('p5'))} / {_p(dist.get('p95'))} | **{m['verdict']['label']}** |")
    c = d["consolidated"]
    L += ["", f"**Consolidado:** {c['strategies']} estrategias, capital US${c['capital_total_usd']:.0f} "
          f"(separado), ejecutadas {c['executed']}, rentables {c['profitable']}, neto simulado "
          f"{_u(c['net_simulated_usd'])}, realizado en ledgers {_u(c['realized_usd'])}.", ""]
    L += ["## Por categoría pedida", ""]
    for cat, ns in d["categories"].items():
        parts = [f"{n}: {d['strategies'][n]['verdict']['label']}" for n in ns if n in d["strategies"]]
        L.append(f"- **{cat}** — " + ("; ".join(parts) or "no corrió en esta ejecución"))
    ext = d["external"]
    L += ["", "## Evidencia externa (no recalculada)", ""]
    for k, v in ext.items():
        if isinstance(v, dict):
            L.append(f"- {k}: " + ", ".join(f"{a}={b}" for a, b in v.items()
                                           if a in ("cycles", "opportunities", "net_positive",
                                                    "executable", "pnl_realized", "phase0_decisions",
                                                    "source")))
    L += ["", "## Detalle", ""]
    for n, m in d["strategies"].items():
        oos, st = m["out_of_sample"], m["stress"]
        L += [f"### {n}", "",
              f"- Veredicto: **{m['verdict']['label']}** — {m['verdict']['why']}",
              f"- Motivos: {', '.join(f'{k}={v}' for k, v in m['reasons'].items()) or 'ninguno'}",
              f"- Pérdidas: {m['losses']['n']} ({_u(m['losses']['usd'])})",
              f"- Duración (ticks con neto estimado > 0): {m['duration_ticks'] or 'n/d'}",
              f"- Períodos (10 min): {m['periods']['n']}, positivos {_p(m['periods']['positive_share'], 0)}",
              f"- Estrés x1.5: estimadas > 0 {st['1.5']['estimated_positive']}, neto sim. "
              f"{_u(st['1.5']['simulated_net'])} · x2: {st['2.0']['estimated_positive']}, "
              f"{_u(st['2.0']['simulated_net'])}",
              f"- Fuera de muestra: {oos}",
              f"- Ledger: {m['ledger']}", ""]
    L += ["## Errores de fuentes", "", f"Total: {d['errors']['total']}"]
    L += [f"- {k}: {v}" for k, v in d["errors"]["by_source"].items()]
    return "\n".join(L) + "\n"


def write_report(d):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    slim = json.loads(json.dumps(d, default=str))
    for m in slim["strategies"].values():
        m["periods"].pop("values", None)
    (REPORT_DIR / "lab_summary.json").write_text(json.dumps(slim, indent=1, ensure_ascii=False),
                                                 encoding="utf-8")
    (REPORT_DIR / "lab_report.md").write_text(render_markdown(d), encoding="utf-8")


def ntfy_text(d):
    c = d["consolidated"]
    lines = [f"{n}: ejec {m['evidence']['simulated_executed']}, rent "
             f"{m['evidence']['simulated_profitable']}, neto {_u(m['net_simulated_usd'])} "
             f"-> {m['verdict']['label']}" for n, m in d["strategies"].items()]
    lines.append(f"Consolidado: neto sim {_u(c['net_simulated_usd'])}, errores {d['errors']['total']}")
    return "[LAB] Pie a pie: resumen del laboratorio", "\n".join(lines)
