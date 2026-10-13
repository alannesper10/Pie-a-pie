"""Auditoría de oportunidades Kalshi antes de abrir cualquier posición paper.

Para cada oportunidad con neto estimado > 0:
  1. vuelve a pedir el libro de CADA pata después de la latencia (T1),
  2. verifica que el volumen completo se llena a precios <= límite planificado
     (orden IOC por pata), con un tope de desfase entre la 1a y la última,
  3. arma la tabla de escenarios (pago en TODOS los resultados),
  4. aplica estrés x1.5 a los costos supuestos (coeficiente de comisión 0.07 y
     slippage no verificados),
  5. estima el costo de que falle una pata (deshacer al bid),
  6. clasifica y guarda la evidencia (libros T0 y T1 crudos) en evidence/.
Solo ARBITRAJE_GARANTIZADO puede abrir posición paper.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from .event_arbitrage import take_from_ladder, taker_fee
from .guarantee import (
    COST_STRESS, EXEC_VERIFIED, GUARANTEED, classify, scenario_table,
    simulate_leg_failure, verify_execution,
)
from .strategies.kalshi_common import asks_for, parse_book

EVIDENCE = Path("evidence") / "kalshi"
AUDIT_FIELDS = [
    "timestamp", "strategy", "event_ticker", "key", "classification", "reason",
    "coverage_method", "n_legs", "contracts", "outlay", "net_expected", "net_min",
    "net_max", "max_loss", "net_min_stressed", "undetermined_scenarios",
    "exec_status", "exec_reason", "skew_s", "leg_fail_loss", "fees_status", "evidence",
]
LEG_FAIL_PROB = 0.02     # ASSUMED, para el costo esperado de ejecución


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def fetch_book(client, ticker, timeout=10.0):
    """Libro crudo + parseado + hora exacta de la consulta."""
    data = client.get_orderbook(ticker, timeout=timeout)
    return {"raw": data, "book": parse_book(data), "fetched_at": now_iso()}


def refetch_after_latency(client, tickers, latency_s, sleep=time.sleep):
    sleep(latency_s)
    return {t: fetch_book(client, t) for t in tickers}


def audit_opportunity(*, client, strategy, event_ticker, key, tickers, sides, contracts,
                      t0_books, outcomes_fn, net_expected, fee_coef, slippage_per_contract,
                      coverage, ts, latency_s=0.5, sleep=time.sleep, evidence_dir=EVIDENCE,
                      t1_books=None):
    """-> dict de auditoría (incluye 'classification'). No abre posiciones."""
    fee_fn = lambda fills: taker_fee(fills, fee_coef)  # noqa: E731
    n = len(tickers)
    t0_ladders = [asks_for(t0_books[t]["book"], s) for t, s in zip(tickers, sides)]
    limits = []
    for lad in t0_ladders:
        fills = take_from_ladder(lad, contracts) if lad else None
        limits.append(fills[-1][0] if fills else None)
    outlay_t0 = fees_t0 = None
    if all(l is not None for l in limits):
        f0 = [take_from_ladder(l, contracts) for l in t0_ladders]
        fees_t0 = sum(fee_fn(f) for f in f0)
        outlay_t0 = (sum(p * q for f in f0 for p, q in f) + fees_t0
                     + contracts * n * slippage_per_contract)

    if t1_books is None:
        t1_books = refetch_after_latency(client, tickers, latency_s, sleep)
    legs = [{"ticker": t, "side": s, "limit": lim if lim is not None else -1.0,
             "asks_after": asks_for(t1_books[t]["book"], s),
             "fetched_after": t1_books[t]["fetched_at"]}
            for t, s, lim in zip(tickers, sides, limits)]
    ex = verify_execution(legs, contracts, fee_fn)

    slip = contracts * n * slippage_per_contract
    if ex["status"] == EXEC_VERIFIED:
        outlay, fees = ex["cost"] + ex["fees"] + slip, ex["fees"]
    else:
        outlay, fees = outlay_t0, fees_t0
    table = scenario_table(outcomes_fn(contracts), outlay) if outlay else None
    net_min = table["net_min"] if table else None
    assumed = (fees if fees is not None else 0.0) + slip
    stressed = None if net_min is None else net_min - (COST_STRESS - 1) * assumed

    leg_fail_loss = None
    if ex.get("legs") and ex["status"] == EXEC_VERIFIED and n > 1:
        bids = lambda t, s: [(p, q) for p, q in t1_books[t]["book"]["yes_bids" if s == "yes" else "no_bids"]]  # noqa: E731
        leg_fail_loss = simulate_leg_failure(ex["legs"], bids, fail_index=n - 1, fee_fn=fee_fn)

    classification, why = classify(
        net_expected=(table["net_max"] if table else net_expected),
        coverage_proven=bool(coverage.get("proven")), exec_status=ex["status"],
        net_min=net_min, net_min_stressed=stressed)

    evidence_dir = Path(evidence_dir) / strategy / ts[:10]
    evidence_dir.mkdir(parents=True, exist_ok=True)
    safe = key.replace("|", "__").replace("/", "_")
    ev_path = evidence_dir / f"{ts[11:19].replace(':', '')}_{safe}.json"
    ev_path.write_text(json.dumps({
        "timestamp": ts, "strategy": strategy, "event_ticker": event_ticker, "key": key,
        "classification": classification, "reason": why, "coverage": coverage,
        "contracts": contracts, "sides": sides, "limits": limits,
        "t0_books": {t: {"fetched_at": b["fetched_at"], "raw": b["raw"]} for t, b in t0_books.items()},
        "t1_books": {t: {"fetched_at": b["fetched_at"], "raw": b["raw"]} for t, b in t1_books.items()},
        "execution": ex, "scenarios": table, "net_min_stressed": stressed,
        "leg_fail_loss": leg_fail_loss,
        "costs": {"fees": {"value": fees, "status": "ASSUMED (coef 0.07; fee_type/multiplier verificados por API de series)"},
                  "slippage": {"value": slip, "status": "ASSUMED"}},
    }, indent=1, default=str), encoding="utf-8")

    return {
        "classification": classification, "reason": why,
        "coverage_method": coverage.get("method"), "n_legs": n, "contracts": contracts,
        "outlay": outlay, "net_expected": net_expected,
        "net_min": net_min, "net_max": table["net_max"] if table else None,
        "max_loss": table["max_loss"] if table else None, "net_min_stressed": stressed,
        "undetermined_scenarios": ";".join(table["undetermined"]) if table else "",
        "exec_status": ex["status"], "exec_reason": ex.get("reason"),
        "skew_s": ex.get("skew_s"), "leg_fail_loss": leg_fail_loss,
        "fees_status": "ASSUMED", "evidence": str(ev_path).replace("\\", "/"),
        "exec": ex, "guaranteed": classification == GUARANTEED,
    }


def audit_row(ts, strategy, event_ticker, key, a):
    return {"timestamp": ts, "strategy": strategy, "event_ticker": event_ticker, "key": key,
            **{k: a.get(k) for k in AUDIT_FIELDS if k not in ("timestamp", "strategy",
                                                              "event_ticker", "key")}}
