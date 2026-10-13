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


CARRY_PAIRS = ("ETHUSDT", "BTCUSDT")


DELIVERY_HOUR_UTC = 8      # especificación de Binance; se verifica contra las velas


def delivery_check(cq_close_by_open, day_ms, price):
    """Cierre del continuo CQ en la vela que cierra a las 08:00 vs el precio de
    entrega publicado (si la hora es correcta, la diferencia es chica)."""
    c = cq_close_by_open.get(day_ms + (DELIVERY_HOUR_UTC - 1) * HOUR)
    return None if c is None else c / price - 1


def spot_twap_fetch(session, pair, exp_ms):
    """TWAP del spot (velas de 1m) en la media hora previa a la entrega: es lo
    que replica el precio de entrega (promedio del índice de 30 min)."""
    r = session.get("https://api.binance.com/api/v3/klines",
                    params={"symbol": pair, "interval": "1m", "startTime": exp_ms - 30 * 60_000,
                            "endTime": exp_ms - 1, "limit": 30}, timeout=20)
    r.raise_for_status()
    closes = [float(x[4]) for x in r.json()]
    return sum(closes) / len(closes) if len(closes) >= 25 else None


def study_carry(step_hours=24, history=None, session=None):
    import requests
    from . import carry
    s = session or requests.Session()
    history = history or HistoryCache()
    now = int(time.time() * 1000) // HOUR * HOUR
    errors, recs_all, out = [], [], {"pairs": {}}
    try:
        rates = carry.fred_dtb3(s)
    except Exception as e:  # noqa: BLE001
        rates, _ = {}, errors.append(f"FRED DTB3: {e}")
    for pair in CARRY_PAIRS:
        d = s.get("https://fapi.binance.com/futures/data/delivery-price",
                  params={"pair": pair}, timeout=20).json()
        days = {x["deliveryTime"]: float(x["deliveryPrice"]) for x in d}
        since = min(days) - 200 * 24 * HOUR
        series = {}
        for ct in ("CURRENT_QUARTER", "NEXT_QUARTER"):
            f = carry.binance_klines_fetcher(s, "https://fapi.binance.com/fapi/v1/continuousKlines",
                                             {"pair": pair, "contractType": ct, "interval": "1h"})
            r = history.ensure("binance_cont", f"{pair}:{ct}", "1h", since, now, f)
            errors += r["errors"]
            series[ct] = history.bars("binance_cont", f"{pair}:{ct}", "1h")
        f = carry.binance_klines_fetcher(s, "https://api.binance.com/api/v3/klines",
                                         {"symbol": pair, "interval": "1h"})
        r = history.ensure("binance_spot_rest", pair, "1h", since, now, f)
        errors += r["errors"]
        spot = history.closes("binance_spot_rest", pair, "1h")
        cq = {b[0]: b[4] for b in series["CURRENT_QUARTER"]}
        deliveries, checks, twap = {}, [], {}
        for day, px in sorted(days.items()):
            exp = day + DELIVERY_HOUR_UTC * HOUR
            deliveries[exp] = px
            try:
                twap[exp] = spot_twap_fetch(s, pair, exp)
            except Exception as e:  # noqa: BLE001
                errors.append(f"TWAP {pair} {exp}: {e}")
            checks.append({"expiry": exp, "cq_close_vs_delivery": delivery_check(cq, day, px),
                           "spot_twap_vs_delivery": (twap[exp] / px - 1) if twap.get(exp) else None})
        twap = {k: v for k, v in twap.items() if v}
        expiries = sorted(deliveries)
        # marcas de tiempo al CIERRE de la vela (apertura + 1h)
        sp = {t + HOUR: c for t, c in spot.items()}
        prices = carry.ContractPrices(
            {code: ({b[0] + HOUR: b[4] for b in series[ct]}, {b[0] + HOUR: b[2] for b in series[ct]})
             for ct, code in (("CURRENT_QUARTER", "CQ"), ("NEXT_QUARTER", "NQ"))}, expiries)
        res = {}
        for code in ("CQ", "NQ"):
            sens = {}
            for m in (1.5, 2.0):
                with carry.fee_scale(m):
                    sens[f"fees_x{m}"] = carry.rule_eval(
                        carry.simulate(sp, prices, deliveries, expiries, rates, step_hours, code, twap))
            recs = carry.simulate(sp, prices, deliveries, expiries, rates, step_hours, code, twap)
            for r_ in recs:
                r_["pair"] = pair
            recs_all += recs
            res[code] = carry.summarize(recs)
            res[code]["sensitivity"] = sens
        out["pairs"][pair] = {"delivery_checks": checks, "bars": {k: len(v) for k, v in series.items()},
                              "spot_bars": len(spot), "results": res}
    out.update({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "step_hours": step_hours, "errors": errors,
                "costs": {"spot_taker": carry.SPOT_TAKER, "fut_taker": carry.FUT_TAKER,
                          "settle_fee": carry.SETTLE_FEE, "half_spread": carry.HALF_SPREAD,
                          "mmr": carry.MMR, "status": "ASSUMED (nivel base público, sin cuenta)"},
                "benchmark": "FRED DTB3 (letra EE.UU. 3 meses), mismo plazo, sin anualizar",
                "results": recs_all})
    # detalle completo (todas las entradas) solo en lab_data/; a reports/ va el resumen
    full = Path("lab_data") / "research"
    full.mkdir(parents=True, exist_ok=True)
    (full / "research_carry.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    slim = {k: v for k, v in out.items() if k != "results"}
    slim["results_note"] = f"{len(recs_all)} entradas simuladas; detalle en lab_data/research/"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "research_carry.json").write_text(json.dumps(slim, indent=1, default=str,
                                                       ensure_ascii=False), encoding="utf-8")
    return out


def study_ccl(db=Path("lab_data") / "watch.sqlite", runs=None):
    """Diferenciales MEP/CCL entre emisoras sobre las recolecciones con fuente ccl."""
    from ..store import LabStore
    from . import ccl
    store = LabStore(db)
    runs = runs or [r for (r,) in store.db.execute(
        "SELECT run_id FROM runs WHERE mode='collect' AND args LIKE '%ccl%' ORDER BY started")]
    obs, ratio, ticks = [], {}, 0
    for run in runs:
        for snap in store.iter_snapshots(run):
            if not snap.ccl:
                continue
            ticks += 1
            for o in ccl.analyze_snapshot(snap):
                o["run"] = run
                obs.append(o)
            for k, v in ccl.ratio_check(snap).items():
                ratio.setdefault(k, {"CONSISTENTE": 0, "NO_CONSISTENTE": 0})[v["status"]] += 1
    eps = ccl.episodes(obs)
    out = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": runs,
           "ticks_with_ccl": ticks, "summary": ccl.summarize(obs), "ratio_check": ratio,
           "episodes_potencial": eps,
           "costs": {"byma_market_fee": ccl.BYMA_MARKET_FEE, "byma_status": "VERIFICADO (BYMA, 5 pb + IVA)",
                     "broker_ar": ccl.BROKER_AR, "broker_us": ccl.BROKER_US,
                     "broker_status": "ASSUMED (varía por broker)"},
           "limitations": ["data912 es una API de terceros: su demora respecto del mercado no está verificada",
                           "BYMA gratuito tiene ~20 min de demora: cruces con Nasdaq son NO_VERIFICABLE",
                           "solo mejor punta: sin profundidad",
                           "normas cambiarias vigentes (plazos mínimos de tenencia, cruces entre monedas) NO verificadas"]}
    full = Path("lab_data") / "research"
    full.mkdir(parents=True, exist_ok=True)
    (full / "research_ccl.json").write_text(json.dumps({**out, "observations": obs}, indent=1,
                                                       default=str), encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "research_ccl.json").write_text(json.dumps(out, indent=1, default=str, ensure_ascii=False),
                                           encoding="utf-8")
    return out
