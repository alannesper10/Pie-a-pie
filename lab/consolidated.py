"""Reporte consolidado de TODAS las familias (A-I + Kalshi + funding Fase 0).

Lee los resultados ya calculados (no recalcula ni descarga nada) y arma una
tabla comparativa con las categorías SEPARADAS: nunca suma garantizadas con
estadísticas, no ejecutables, no verificables o sin edge.
"""

import json
from pathlib import Path

OUT = Path("reports") / "lab"
FAMILY = {
    "cross_exchange": "A. Entre exchanges (CEX)", "triangular": "B. Triangular (3-4 patas)",
    "basis_funding": "C. Basis/funding perpetuo", "polymarket_buy_all_no": "D. Predicción: Polymarket NO",
    "prediction_cross_venue": "D. Predicción: Kalshi~Polymarket", "cex_dex": "E. CEX vs DEX (Jupiter)",
    "cash_and_carry": "F. Spot vs futuro con vencimiento", "calendar_spread": "F. Calendar spread",
    "liquidity_provision": "I. Provisión de liquidez",
}
CATS = ("ARBITRAJE_GARANTIZADO", "ESTADISTICA", "NO_EJECUTABLE", "NO_VERIFICABLE", "SIN_EDGE")


def _load(name):
    p = OUT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def build():
    lab = _load("lab_summary.json") or {}
    rows = []
    for name, m in (lab.get("strategies") or {}).items():
        cats = {c: (m.get("by_category") or {}).get(c, {}).get("n", 0) for c in CATS}
        rows.append({"familia": FAMILY.get(name, name), "estrategia": name,
                     "evidencia": f"{lab.get('run', {}).get('source_run') or lab.get('run', {}).get('run_id')}",
                     "observadas": m["evidence"]["observed"], **cats,
                     "neto_contado_usd": m["net_simulated_usd"],
                     "veredicto": m["verdict"]["label"]})
    research = {}
    for key, fam in (("stat_arb", "H. Pares cointegrados"), ("etf", "G. ETF / CCL"),
                     ("imbalance", "I. Desbalance del libro"), ("discovery", "Descubrimiento")):
        d = _load(f"research_{key}.json")
        if not d:
            continue
        if key == "etf":
            res = d["etf"]["results"] + d["ccl"]["results"]
            tested = d["etf"]["pairs_tested"] + d["ccl"]["pairs_tested"]
            bh = d["etf"]["bh_rejections"] + d["ccl"]["bh_rejections"]
        elif key == "discovery":
            res, tested, bh = d["results"], d["funnel"]["tested"], d["funnel"]["bh_train"]
        else:
            res = d["results"]
            tested = d.get("pairs_tested") or d.get("hypotheses_tested")
            bh = d["bh_rejections"]
        verdicts = {}
        if key == "etf":
            for part in ("etf", "ccl"):
                for v, n in (d[part].get("verdict_counts_all") or {}).items():
                    verdicts[v] = verdicts.get(v, 0) + n
        verdicts = verdicts or dict(d.get("verdict_counts_all") or {})
        if not verdicts:       # resumen viejo sin conteos: se cuentan las filas presentes
            for r in res:
                v = r.get("verdict") or ("PROMOVIDA" if r.get("promoted") else "NO_PROMOVIDA")
                verdicts[v] = verdicts.get(v, 0) + 1
        research[key] = {"familia": fam, "probadas": tested, "sobreviven_BH": bh,
                         "veredictos": verdicts}
    ext = {}
    try:
        from src.compare import build as cmp
        c = cmp("data", "reports/funding_basis")
        for k in ("kalshi_current", "buy_all_no", "strike_inconsistency", "funding_basis"):
            ext[k] = {x: c[k].get(x) for x in ("cycles", "opportunities", "net_positive",
                                               "executable", "pnl_realized")}
    except Exception as e:  # noqa: BLE001
        ext["error"] = str(e)
    return {"lab": rows, "research": research, "external": ext,
            "lab_run": lab.get("run"), "errors": lab.get("errors")}


def render(d):
    L = ["# Pie a Pie — comparación consolidada de familias", "",
         "Categorías SEPARADAS (nunca sumadas entre sí). Todo es simulación paper.", "",
         "## Familias de mercado (laboratorio, corrida " + str((d['lab_run'] or {}).get('source_run')) + ")", "",
         "| Familia | Observadas | Garantizadas | Estadísticas | No ejecutables | No verificables | Sin edge | Neto contado US$ | Veredicto |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in d["lab"]:
        L.append(f"| {r['familia']} | {r['observadas']} | {r['ARBITRAJE_GARANTIZADO']} | {r['ESTADISTICA']} | "
                 f"{r['NO_EJECUTABLE']} | {r['NO_VERIFICABLE']} | {r['SIN_EDGE']} | "
                 f"{r['neto_contado_usd']:+.4f} | {r['veredicto']} |")
    L += ["", "## Familias estadísticas e hipótesis", "",
          "| Estudio | Probadas | Sobreviven BH | Veredictos |", "|---|---|---|---|"]
    for k, r in d["research"].items():
        L.append(f"| {r['familia']} | {r['probadas']} | {r['sobreviven_BH']} | {r['veredictos']} |")
    L += ["", "## Kalshi (GitHub Actions) y funding Fase 0 — solo lectura", "",
          "| Estrategia | Ciclos | Oportunidades | Net-positive | Ejecutables | P&L realizado |",
          "|---|---|---|---|---|---|"]
    for k, r in d["external"].items():
        if isinstance(r, dict):
            L.append(f"| {k} | {r.get('cycles')} | {r.get('opportunities')} | {r.get('net_positive')} | "
                     f"{r.get('executable')} | {r.get('pnl_realized')} |")
    return "\n".join(L) + "\n"


def write():
    d = build()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "consolidated.json").write_text(json.dumps(d, indent=1, default=str, ensure_ascii=False),
                                           encoding="utf-8")
    (OUT / "consolidated.md").write_text(render(d), encoding="utf-8")
    return d
