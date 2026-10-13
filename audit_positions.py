"""Auditoría de SOLO LECTURA de las posiciones paper abiertas de kalshi_current.

No modifica data/ (ledger, historial) ni cierra posiciones. Reconstruye cada
posición desde el ledger + el historial de git (caché de eventos del ciclo de
apertura) + la API pública (reglas y libros actuales), y escribe
reports/audit/open_positions.{md,json} con una recomendación por posición.

  python audit_positions.py
"""

import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from src.guarantee import kalshi_yes_coverage, scenario_table, yes_all_outcomes
from src.kalshi_public import KalshiPublicClient
from src.strategies.kalshi_common import parse_book

OUT = Path("reports") / "audit"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          encoding="utf-8").stdout


def fee(q, p):
    return math.ceil(round(0.07 * q * p * (1 - p) * 100, 9)) / 100


def opening_commit(pos):
    shas = git("log", "--format=%H", "-S", f"{pos['opened_at']},OPEN,{pos['event_ticker']}",
               "--", "data/paper_trades.csv").split()
    return shas[-1] if shas else None


def legs_at(sha, event_ticker):
    cache = json.loads(git("show", f"{sha}:data/events_cache.json") or "{}")
    ev = next((e for e in cache.get("events", []) if e["event_ticker"] == event_ticker), None)
    cyc = [l for l in git("show", f"{sha}:data/cycles.csv").splitlines()]
    return cache.get("refreshed_at"), ev, cyc[-1] if cyc else None


def audit(pos, client):
    out = {"event_ticker": pos["event_ticker"], "opened_at": pos["opened_at"],
           "contracts": pos["contracts"], "cost": pos["cost"], "fees": pos["fees"],
           "slippage": pos["slippage"],
           "outlay": pos["cost"] + pos["fees"] + pos["slippage"],
           "expected_net_recorded": pos["expected_net"], "legs": pos["legs"],
           "expected_close": pos["expected_close"]}
    sha = opening_commit(pos)
    out["opening_commit"] = sha
    if sha:
        refreshed, ev, cyc = legs_at(sha, pos["event_ticker"])
        out["cache_refreshed_at"] = refreshed
        out["cycle_row"] = cyc
        out["legs_at_open"] = [{"ticker": m["ticker"], "name": m.get("yes_sub_title"),
                                "yes_ask": float(m["yes_ask_dollars"]),
                                "ask_size": m.get("yes_ask_size_fp"),
                                "fee_c": fee(pos["contracts"], float(m["yes_ask_dollars"]))}
                               for m in (ev or {}).get("legs", [])]
        out["coverage_at_open"] = (ev or {}).get("exhaustive_reason")
    d = client.get(f"events/{pos['event_ticker']}", params={"with_nested_markets": "true"})
    e = d.get("event", d)
    e.setdefault("markets", d.get("markets"))
    cov = kalshi_yes_coverage(e, manual={})
    out["title"] = e.get("title")
    out["coverage_now"] = cov.to_dict()
    out["scenarios"] = scenario_table(yes_all_outcomes(pos["contracts"], cov), out["outlay"])
    # Valor de salida HOY: vender cada pata al YES bid (libro actual) con comisión.
    exit_value, legs_now = 0.0, []
    for t in pos["legs"]:
        m = next((x for x in e["markets"] if x["ticker"] == t), {})
        b = parse_book(client.get_orderbook(t))
        need, got, proceeds = pos["contracts"], 0.0, 0.0
        for p, q in b["yes_bids"]:
            take = min(q, need - got)
            got += take
            proceeds += take * p
            if got >= need - 1e-9:
                break
        f = fee(got, proceeds / got) if got else 0.0
        exit_value += proceeds - f
        legs_now.append({"ticker": t, "status": m.get("status"), "result": m.get("result"),
                         "best_yes_bid": b["yes_bids"][0][0] if b["yes_bids"] else None,
                         "sellable": got, "proceeds": round(proceeds, 4), "fee": f})
    out["legs_now"] = legs_now
    out["exit_value_now"] = round(exit_value, 4)
    out["mark_to_market_pnl"] = round(exit_value - out["outlay"], 4)
    out["fully_sellable_now"] = all(l["sellable"] >= pos["contracts"] - 1e-9 for l in legs_now)
    return out


def recommendation(a):
    s = a["scenarios"]
    return (f"Reclasificar como ESPECULATIVA (cobertura {a['coverage_now']['method']}): gana "
            f"{s['net_max']:+.3f} si gana una película listada y pierde {s['max_loss']:.3f} si "
            f"gana una no listada. NO cerrar automáticamente: cerrarla hoy en paper realizaría "
            f"{a['mark_to_market_pnl']:+.3f} USD (vender las 16 patas al bid, "
            f"{'todas vendibles' if a['fully_sellable_now'] else 'NO todas vendibles por profundidad'}). "
            f"Opción recomendada: mantenerla abierta SIN tocar el ledger, marcada en "
            f"reports/audit como posición especulativa abierta por error y EXCLUIDA de las "
            f"métricas de arbitraje; registrar su resultado real al liquidarse como evidencia "
            f"del riesgo. Cerrarla (y cómo registrarlo) requiere tu decisión explícita.")


def main():
    client = KalshiPublicClient()
    state = json.loads(Path("data/state.json").read_text(encoding="utf-8"))
    paper = state["paper"]
    audits = [audit(p, client) for p in paper["open"]]
    for a in audits:
        a["recommendation"] = recommendation(a)
    summary = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "ledger_cash": paper["cash"],
               "ledger_locked": sum(a["outlay"] for a in audits),
               "ledger_check": round(100 - sum(a["outlay"] for a in audits) - paper["cash"], 6),
               "positions": audits}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "open_positions.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False,
                                                       default=str), encoding="utf-8")
    L = ["# Auditoría de posiciones paper abiertas (kalshi_current)", "",
         f"Generado: {summary['generated_at']} · solo lectura (ledger sin cambios)", "",
         f"Caja {paper['cash']:.4f} · bloqueado {summary['ledger_locked']:.4f} · "
         f"control 100 - bloqueado - caja = {summary['ledger_check']}", ""]
    for a in audits:
        s = a["scenarios"]
        L += [f"## {a['event_ticker']} — {a['title']}", "",
              f"- Abierta {a['opened_at']} (commit {str(a['opening_commit'])[:7]}), "
              f"{a['contracts']} contratos, {len(a['legs'])} patas YES",
              f"- Inversión: costo {a['cost']} + comisiones {a['fees']} + slippage "
              f"{a['slippage']:.3f} = **{a['outlay']:.3f}**",
              f"- Cobertura al abrir: {a.get('coverage_at_open')} → hoy: "
              f"**{a['coverage_now']['method']}** ({'; '.join(a['coverage_now']['reasons'][-1:])})",
              f"- Evidencia de lista abierta: {len(a['coverage_now']['open_list_evidence'])} patas "
              f"(ej. {a['coverage_now']['open_list_evidence'][:1]})", "",
              "| Escenario | Pago | Neto |", "|---|---|---|"]
        for r in s["scenarios"]:
            L.append(f"| {r['scenario']} | {r['payout'] if r['payout'] is not None else 'precio justo (no determinable)'} | "
                     f"{'n/d' if r['net'] is None else f'{r[chr(110)+chr(101)+chr(116)]:+.3f}'} |")
        L += ["", f"- Pérdida máxima: **{s['max_loss']:.3f} USD** · ganancia máxima {s['net_max']:+.3f}",
              f"- Valor de salida hoy (vender al bid): {a['exit_value_now']:.3f} → P&L a mercado "
              f"**{a['mark_to_market_pnl']:+.3f}**",
              "", "| Pata | Ask al abrir | Tam. | Comisión | Estado hoy | Bid hoy |",
              "|---|---|---|---|---|---|"]
        now = {l["ticker"]: l for l in a["legs_now"]}
        for l in a.get("legs_at_open", []):
            n = now.get(l["ticker"], {})
            L.append(f"| {l['ticker'].split('-')[-1]} {l['name']} | {l['yes_ask']:.2f} | "
                     f"{l['ask_size']} | {l['fee_c']:.2f} | {n.get('status')} {n.get('result') or ''} | "
                     f"{n.get('best_yes_bid')} |")
        L += ["", f"**Recomendación:** {a['recommendation']}", ""]
    (OUT / "open_positions.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
