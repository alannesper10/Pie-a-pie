"""Ejecución de los estudios estadísticos y reporte. Separa recolección (caché
incremental), evaluación y reporte; nada se vuelve a descargar si ya está."""

import json
import math
import sqlite3
import time
from pathlib import Path

from ..history import HistoryCache, yahoo_fetcher
from . import etf as etf_mod
from . import imbalance as imb_mod
from . import stat_arb as sa

OUT = Path("reports") / "lab"
UNIVERSE = ("BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT",
            "DOGE/USDT", "AVAX/USDT", "LINK/USDT", "LTC/USDT")
HOUR = 3_600_000


TOP_IN_REPORT = 50


def _write(name, data):
    """Detalle completo en lab_data/ (fuera de git); a reports/ va un resumen:
    totales + las TOP_IN_REPORT filas de menor p + todas las promovidas."""
    full = Path("lab_data") / "research"
    full.mkdir(parents=True, exist_ok=True)
    (full / f"research_{name}.json").write_text(json.dumps(data, indent=1, default=str,
                                                           ensure_ascii=False), encoding="utf-8")
    slim = dict(data)
    res = data.get("results")
    if isinstance(res, list):   # conteos SIEMPRE sobre todas las filas, no sobre el recorte
        counts = {}
        for r in res:
            v = r.get("verdict") or ("PROMOVIDA" if r.get("promoted") else "NO_PROMOVIDA")
            counts[v] = counts.get(v, 0) + 1
        slim["verdict_counts_all"] = counts
    if isinstance(res, list) and len(res) > TOP_IN_REPORT:
        key = "p_train" if res and "p_train" in res[0] else "p"
        ordered = sorted(res, key=lambda r: r.get(key, 1.0))
        keep = ordered[:TOP_IN_REPORT] + [r for r in ordered[TOP_IN_REPORT:] if r.get("promoted")
                                          or r.get("verdict") == "ESTADISTICA"]
        slim["results"] = keep
        slim["results_note"] = (f"{len(res)} filas en total; se muestran {len(keep)} (menor p y "
                                f"todas las promovidas). Detalle completo: lab_data/research/")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"research_{name}.json").write_text(json.dumps(slim, indent=1, default=str,
                                                          ensure_ascii=False), encoding="utf-8")


def crypto_hourly(days=120, now_ms=None, history=None):
    import ccxt
    now_ms = now_ms or int(time.time() * 1000) // HOUR * HOUR
    history = history or HistoryCache()
    ex = ccxt.binance({"enableRateLimit": True, "timeout": 20000})
    closes, errors = sa.load_universe(history, ex, UNIVERSE, days, now_ms)
    return closes, errors


def study_stat_arb(days=120):
    closes, errors = crypto_hourly(days)
    ts, series = sa.align(closes)
    res = sa.evaluate_pairs(series, len(ts))
    res.update({"source": "binance spot 1h (caché incremental)", "days": days,
                "symbols": sorted(series), "errors": errors,
                "from": ts[0] if ts else None, "to": ts[-1] if ts else None})
    _write("stat_arb", res)
    return res


def study_etf(days=730):
    now = int(time.time() * 1000) // 86_400_000 * 86_400_000
    h = HistoryCache()
    tickers = sorted({t for g in etf_mod.ETF_GROUPS.values() for t in g}
                     | set(etf_mod.ADR_RATIOS) | {v[0] for v in etf_mod.ADR_RATIOS.values()})
    errors, closes = [], {}
    for t in tickers:
        r = h.ensure("yahoo", t, "1d", now - days * 86_400_000, now, yahoo_fetcher(t))
        errors += r["errors"]
        c = h.closes("yahoo", t, "1d")
        if c:
            closes[t] = c
        time.sleep(0.3)
    etf_res = etf_mod.evaluate_relations(closes, etf_mod.etf_pairs(), kind="ETF")
    ccl, checks = etf_mod.ccl_series(closes)
    from itertools import combinations
    ccl_res = etf_mod.evaluate_relations(ccl, list(combinations(sorted(ccl), 2)),
                                         etf_mod.RelationConfig(cost_per_execution=0.005),
                                         kind="CCL")
    res = {"source": "Yahoo Finance (cierres diarios)", "days": days, "errors": errors,
           "etf": etf_res, "ccl_checks": checks, "ccl": ccl_res,
           "ccl_cost_note": "0.5% por ejecución ASSUMED (comisiones BYMA + spread)"}
    _write("etf", res)
    return res


def study_imbalance(db=Path("lab_data") / "lab.sqlite"):
    from ..store import LabStore
    st = LabStore(db)
    runs = [r for (r,) in st.db.execute(
        "SELECT run_id FROM runs WHERE mode IN ('live','collect') ORDER BY started")]
    series = {}
    for r in runs:     # cada corrida por separado: los ticks no se mezclan entre corridas
        for k, v in imb_mod.collect_series(st.iter_snapshots(r)).items():
            series[(k[0], f"{k[1]}@{r}")] = v
    res = imb_mod.evaluate(series)
    res.update({"runs": runs, "ticks_total": sum(len(v) for v in series.values())})
    _write("imbalance", res)
    return res


def _funding_markets(path=Path("funding_data") / "funding.sqlite"):
    if not path.exists():
        return []
    db = sqlite3.connect(path)
    out = []
    for ex, asset in db.execute("SELECT DISTINCT exchange, asset FROM funding_history"):
        prices = db.execute("SELECT ts, close FROM price_history WHERE exchange=? AND asset=? "
                            "AND market='perp' ORDER BY ts", (ex, asset)).fetchall()
        if len(prices) < 500:
            continue
        idx = {ts: i for i, (ts, _) in enumerate(prices)}
        fund = {idx[ts]: r for ts, r in db.execute(
            "SELECT ts, rate FROM funding_history WHERE exchange=? AND asset=?", (ex, asset))
            if ts in idx}
        out.append((f"{ex}|{asset}", [c for _, c in prices], fund))
    return out


def study_discovery(stat_arb_res=None, imbalance_res=None):
    from .. import discovery as d
    closes, errors = crypto_hourly(120)
    ts, _ = sa.align(closes)
    hyps = []
    for s in sorted(closes):
        series = [closes[s][t] for t in ts]
        hyps += d.momentum_hypotheses(s.split("/")[0], series)
    for name, perp, fund in _funding_markets():
        hyps += d.funding_hypotheses(name, perp, fund)
    ext = []
    for r in (stat_arb_res or {}).get("results", []):
        o = r.get("oos") or {}
        ext.append(d.external_hypothesis(f"pares|{r['pair']}", "pares_cointegrados", r["p"],
                                         r["discovery_trades"], o.get("trades", 0),
                                         o.get("net_sum", 0.0), o.get("net_sum_costs_x1.5", 0.0)))
    for r in (imbalance_res or {}).get("results", []):
        ext.append(d.external_hypothesis(f"imb|{r['market']}|{r['theta']}", "desbalance_libro",
                                         r["p"], r["train_trades"], r["test_trades"],
                                         (r["test_net_mean"] or 0) * r["test_trades"], 0.0))
    res = d.run_discovery(hyps, ext, registry=d.Registry())
    res["errors"] = errors
    res["results"] = sorted(res["results"], key=lambda r: r["p_train"])
    _write("discovery", res)
    return res


def run_all():
    out = {}
    for name, fn in (("stat_arb", study_stat_arb), ("etf", study_etf),
                     ("imbalance", study_imbalance)):
        try:
            out[name] = fn()
        except Exception as e:  # noqa: BLE001 - un estudio no tumba a los demás
            out[name] = {"error": f"{type(e).__name__}: {e}"}
    try:
        out["discovery"] = study_discovery(out.get("stat_arb"), out.get("imbalance"))
    except Exception as e:  # noqa: BLE001
        out["discovery"] = {"error": f"{type(e).__name__}: {e}"}
    return out
