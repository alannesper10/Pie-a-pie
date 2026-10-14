"""PIE A PIE - laboratorio paralelo de estrategias (SOLO simulación).

  python run_lab.py run --ticks 20 --interval-sec 30 --seed 7   en vivo, guarda snapshots
  python run_lab.py replay --seed 7 [--run RUN_ID]              reproduce sobre snapshots guardados
  python run_lab.py report [--run RUN_ID] [--notify]             informe comparativo
  python run_lab.py suggest-pairs                                candidatas Kalshi~Polymarket (UNVERIFIED)

No envía órdenes ni usa claves. No escribe en data/ (dataset oficial).
Datos crudos: lab_data/lab.sqlite (fuera de git). Reportes: reports/lab/.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

from lab import PAPER_ONLY
from lab.core import ExecConfig
from lab.evaluate import REPORT_DIR, build_report, ntfy_text, write_report
from lab.runner import Lab, build_snapshot
from lab.sources import now_iso
from lab.store import LabStore

DB = Path(os.environ.get("LAB_DB", Path("lab_data") / "lab.sqlite"))
ALL = ("cross_exchange", "triangular", "cex_dex", "cash_and_carry", "calendar_spread",
       "basis_funding", "polymarket_buy_all_no", "prediction_cross_venue",
       "liquidity_provision")
log = logging.getLogger("lab")


def code_version():
    """sha de git del código que generó la corrida (separa resultados de versiones)."""
    import subprocess
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True, timeout=10).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "lab", "run_lab.py"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001
        return "desconocida"


def make_modules(names, run_id, seed, live=True):
    from lab.modules.cross_exchange import CrossExchange
    from lab.modules.liquidity import LiquidityProvision
    from lab.modules.prediction import CrossVenuePrediction, PolymarketBuyAllNo
    from lab.modules.triangular import Triangular
    from lab.modules.cex_dex import CexDex
    from lab.modules.term_structure import CalendarSpread, TermStructure
    out = []
    for n in names:
        if n == "cex_dex":
            out.append(CexDex())
        elif n == "cash_and_carry":
            out.append(TermStructure())
        elif n == "calendar_spread":
            out.append(CalendarSpread())
        elif n == "cross_exchange":
            out.append(CrossExchange())
        elif n == "triangular":
            out.append(Triangular())
        elif n == "polymarket_buy_all_no":
            out.append(PolymarketBuyAllNo())
        elif n == "prediction_cross_venue":
            out.append(CrossVenuePrediction())
        elif n == "liquidity_provision":
            out.append(LiquidityProvision())
        elif n == "basis_funding":
            if not live:
                log.warning("basis_funding no es reproducible (usa datos de perpetuos en vivo): se omite en replay")
                continue
            from lab.modules.basis import BasisFunding
            out.append(BasisFunding(Path("lab_data") / "runs" / f"{run_id}_funding.sqlite", seed=seed))
    return out


def _guard(args):
    from lab.resources import ResourceGuard
    return ResourceGuard(max_rss_mb=args.max_rss_mb,
                         max_seconds=args.max_minutes * 60 if args.max_minutes else None)


def _sources(mods_or_flags):
    from lab.sources import CryptoSource, PolymarketSource
    need_crypto, need_pm, pairs = mods_or_flags
    crypto = CryptoSource() if need_crypto else None
    pm = PolymarketSource() if need_pm else None
    kalshi = None
    if pairs:
        from src.kalshi_public import KalshiPublicClient
        kalshi = KalshiPublicClient()
    return crypto, pm, kalshi


def cmd_collect(args):
    """SOLO recolección: guarda snapshots (checkpoint por tick). Reanudable con
    --resume --run RUN_ID. La evaluación se hace después con `evaluate`."""
    from lab.modules.prediction import load_verified_pairs
    store = LabStore(DB)
    run_id = args.run or f"collect-{time.strftime('%Y%m%dT%H%M%S')}"
    from datetime import datetime, timezone
    from lab.collect_check import last_valid_tick, window_action
    start = 0
    if args.resume and store.run_info(run_id):
        start = last_valid_tick(store.db, run_id) + 1    # una captura ilegible se vuelve a tomar
        log.info("reanudando %s desde el tick %d (última captura válida + 1)", run_id, start)
    else:
        store.start_run(run_id, now_iso(), "collect", args.seed,
                        args={**vars(args), "code_version": code_version()})
    src = set(args.sources.split(","))
    pairs = load_verified_pairs() if "polymarket" in src else []
    crypto, pm, kalshi = _sources(("crypto" in src, "polymarket" in src, pairs))
    from lab.sources import CclSource, FuturesSource, JupiterSource
    dex = JupiterSource() if "dex" in src else None
    futures = FuturesSource() if "futures" in src else None
    ccl = CclSource() if "ccl" in src else None
    guard, markets = _guard(args), {}
    day = datetime.strptime(args.date_art, "%Y-%m-%d").date() if args.date_art else None
    stopped_by_guard = False
    for t in range(start, start + args.ticks):
        if args.window_art:
            action, wait = window_action(datetime.now(timezone.utc), args.window_art, day)
            if action == "wait":
                log.info("esperando la apertura de la ventana %s: %.0f s", args.window_art, wait)
            while action == "wait":          # de a 60 s: si la notebook se suspende, se recalcula con el reloj
                time.sleep(min(wait, 60.0))
                action, wait = window_action(datetime.now(timezone.utc), args.window_art, day)
            if action == "stop":
                log.info("fin de la ventana %s (hora argentina): se detiene en el tick %d",
                         args.window_art, t - 1)
                break
        t0 = time.monotonic()
        snap = build_snapshot(t, crypto, pm, args.latency_ms, markets_cache=markets,
                              pairs=pairs, kalshi_client=kalshi, dex=dex, futures=futures,
                              ccl=ccl, need_trades="crypto" in src)
        store.save_snapshot(run_id, snap)
        ok, why = guard.check()
        log.info("collect %s tick %d | errores %d | %.1fs | memoria pico %.0f MB",
                 run_id, t, len(snap.errors), time.monotonic() - t0, guard.peak_rss)
        del snap
        if not ok:
            log.warning("guardia de recursos: %s. Checkpoint en tick %d; reanudar con "
                        "--resume --run %s", why, t, run_id)
            stopped_by_guard = True
            break
        if t < start + args.ticks - 1:
            time.sleep(max(0.0, args.interval_sec - (time.monotonic() - t0)))
    print(run_id)
    if stopped_by_guard:
        sys.exit(3)                          # el supervisor reanuda con --resume


def cmd_run(args):
    from lab.sources import CryptoSource, PolymarketSource
    store = LabStore(DB)
    run_id = f"live-{time.strftime('%Y%m%dT%H%M%S')}"
    names = args.modules.split(",") if args.modules else ALL
    store.start_run(run_id, now_iso(), "live", args.seed, args=vars(args))
    mods = make_modules(names, run_id, args.seed)
    lab = Lab(mods, store, run_id, ExecConfig(latency_ms=args.latency_ms, seed=args.seed))
    need_crypto = any(getattr(m, "needs_crypto_books", False) for m in mods)
    need_pm = any(getattr(m, "needs_polymarket", False) for m in mods) or \
        any(m.name == "prediction_cross_venue" for m in mods)
    crypto = CryptoSource() if need_crypto else None
    pm = PolymarketSource() if need_pm else None
    from lab.sources import FuturesSource, JupiterSource
    dex = JupiterSource() if any(getattr(m, "needs_dex", False) for m in mods) else None
    futures = FuturesSource() if any(getattr(m, "needs_futures", False) for m in mods) else None
    markets = {}
    pairs = next((m.pairs for m in mods if m.name == "prediction_cross_venue"), [])
    kalshi = None
    if pairs:
        from src.kalshi_public import KalshiPublicClient
        kalshi = KalshiPublicClient()
    log.info("pares Kalshi~Polymarket verificados: %d", len(pairs))
    log.info("run %s: módulos %s", run_id, [m.name for m in mods])
    guard = _guard(args)
    try:
        for t in range(args.ticks):
            t0 = time.monotonic()
            snap = build_snapshot(t, crypto, pm, args.latency_ms, markets_cache=markets,
                                  pairs=pairs, kalshi_client=kalshi, dex=dex, futures=futures)
            store.save_snapshot(run_id, snap)
            counts = lab.run_tick(snap)
            log.info("tick %d: %s | errores de fuentes %d | %.1fs", t, counts, len(snap.errors),
                     time.monotonic() - t0)
            ok, why = guard.check()
            if not ok:
                log.warning("guardia de recursos: %s. Se corta ordenadamente en el tick %d", why, t)
                break
            if t < args.ticks - 1:
                time.sleep(max(0.0, args.interval_sec - (time.monotonic() - t0)))
    except KeyboardInterrupt:
        log.info("Cortado por el usuario.")
    finally:
        lab.finish()
    report(store, run_id, args.notify)


def cmd_replay(args):
    """Evalúa (o re-evalúa) una corrida guardada (live o collect), tick por tick,
    sin cargarla entera en memoria."""
    store = LabStore(DB)
    src = args.run or store.latest_run("collect") or store.latest_run("live")
    if not src:
        sys.exit("No hay corridas guardadas para evaluar.")
    run_id = (f"replay-{src}-s{args.seed}{'-fresh' if args.fresh_ledger else ''}"
              f"-{time.strftime('%H%M%S')}")
    store.start_run(run_id, now_iso(), "replay", args.seed, source_run=src, args=vars(args))
    names = args.modules.split(",") if args.modules else ALL
    first = next(store.iter_snapshots(src), None)
    lab = Lab(make_modules(names, run_id, args.seed, live=False), store, run_id,
              ExecConfig(latency_ms=first.latency_ms if first else 500, seed=args.seed))
    guard, n = _guard(args), 0
    from lab.core import StrategyLedger
    for s in store.iter_snapshots(src):
        if args.fresh_ledger:      # cada tick como si fuera el primero (episodios)
            lab.ledgers = {k: StrategyLedger(k, 100.0) for k in lab.ledgers}
        lab.run_tick(s)
        n += 1
        ok, why = guard.check()
        if not ok:
            log.warning("guardia de recursos: %s. Evaluación parcial hasta el tick %d", why, s.tick)
            break
    lab.finish()
    log.info("evaluación de %s: %d ticks", src, n)
    report(store, run_id, args.notify)


def report(store, run_id, notify=False):
    d = build_report(store, run_id)
    write_report(d)
    print((REPORT_DIR / "lab_report.md").read_text(encoding="utf-8"))
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if notify and topic:
        from src.notify import send
        title, body = ntfy_text(d)
        send(topic, title, body, 2, ["test_tube"])
    return d


def cmd_report(args):
    store = LabStore(DB)
    run_id = args.run or store.latest_run()
    if not run_id:
        sys.exit("No hay corridas.")
    report(store, run_id, args.notify)


def cmd_suggest_pairs(args):
    from lab.modules.prediction import suggest_pairs
    from lab.sources import PolymarketSource
    from src.kalshi_public import KalshiPublicClient
    pm, errs = PolymarketSource(max_events=args.max_events).fetch()
    kc = KalshiPublicClient()
    kev = list(kc.iter_events(status="open", with_nested_markets=True, max_pages=args.kalshi_pages))
    cands = suggest_pairs(kev, pm["events"], top=args.top)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / "prediction_pair_candidates.json"
    out.write_text(json.dumps({"generated_at": now_iso(), "status": "UNVERIFIED",
                               "note": "Revisar reglas, fechas y fuentes de resolución a mano. "
                                       "Para usar un par, copiarlo a config/prediction_pairs.json "
                                       "con verified=true, verified_by y verified_at.",
                               "errors": errs, "candidates": cands}, indent=1,
                              ensure_ascii=False), encoding="utf-8")
    print(f"{len(cands)} candidatas (UNVERIFIED) -> {out}")
    for c in cands[:10]:
        print(f"  {c['score']:.2f} {c['kalshi_ticker']} ~ {c['polymarket_question']}")


def cmd_research(args):
    """Estudios estadísticos (G etf, H stat_arb, I imbalance, descubrimiento)."""
    from lab.research import runner as rr
    fn = {"stat_arb": rr.study_stat_arb, "etf": rr.study_etf, "imbalance": rr.study_imbalance,
          "discovery": rr.study_discovery, "carry": rr.study_carry, "ccl": rr.study_ccl,
          "all": rr.run_all}[args.study]
    res = fn()
    print(json.dumps({k: (v.get("funnel") or v.get("bh_rejections") or v.get("error") or "ok")
                      if isinstance(v, dict) else v for k, v in (res if args.study == "all"
                                                                 else {args.study: res}).items()},
                     indent=1, default=str))


def cmd_pm_gaps(args):
    """Diagnóstico de los casos Polymarket NO_BOOK_FOR_LEG de una corrida guardada."""
    from lab.research.pm_gaps import diagnose_run
    store = LabStore(DB)
    run_id = args.run or store.latest_run("collect")
    r = diagnose_run(store.iter_snapshots(run_id))
    r["run_id"] = run_id
    full = Path("lab_data") / "research"
    full.mkdir(parents=True, exist_ok=True)
    (full / f"polymarket_gaps_{run_id}.json").write_text(
        json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    slim = {k: v for k, v in r.items() if k != "detail"}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / f"polymarket_gaps_{run_id}.json").write_text(
        json.dumps(slim, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: slim[k] for k in ("run_id", "cases", "causes_by_leg", "events",
                                           "gamma_positive_indicative")}, indent=1))


def cmd_episodes(args):
    """Episodios (oportunidades persistentes contadas una vez) de una evaluación."""
    from lab import episodes
    store = LabStore(DB)
    run_id = args.run or store.latest_run("replay")
    src = (store.run_info(run_id) or {}).get("source_run")
    tick_ts = {}
    if src:
        tick_ts = dict(store.db.execute("SELECT tick, ts FROM snapshots WHERE run_id=?", (src,)))
    eps = episodes.build(store.opportunities(run_id), tick_ts)
    out = {"run_id": run_id, "source_run": src,
           "code_version": json.loads((store.run_info(src) or {}).get("args") or "{}").get("code_version")
           if src else None,
           "summary": episodes.summarize(eps), "episodes": eps}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / f"episodes_{src or run_id}.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(out["summary"], indent=1))


def cmd_verify_collect(args):
    """Integridad y continuidad de una corrida de recolección (solo lectura)."""
    from lab.collect_check import verify_run
    store = LabStore(DB)
    src = args.sources.split(",")[0] if args.sources else "ccl"
    out = verify_run(store.db, args.run, interval_sec=args.interval_sec, source=src)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if not out.get("ok"):
        sys.exit(1)


def cmd_consolidate(args):
    from lab.consolidated import write
    write()
    print((REPORT_DIR / "consolidated.md").read_text(encoding="utf-8"))


def main(argv=None):
    if not PAPER_ONLY:
        sys.exit("El laboratorio es solo simulación (PAPER_ONLY).")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["run", "collect", "evaluate", "replay", "report",
                                   "suggest-pairs", "research", "consolidate", "pm-gaps",
                                   "episodes", "verify-collect"])
    p.add_argument("--study", default="all",
                   choices=["stat_arb", "etf", "imbalance", "discovery", "carry", "ccl", "all"])
    p.add_argument("--window-art", default=None,
                   help="collect: recolectar solo dentro de HH:MM-HH:MM hora argentina (p. ej. 11:00-17:05)")
    p.add_argument("--date-art", default=None,
                   help="collect: día (AAAA-MM-DD, hora argentina) de la ventana; por defecto, hoy")
    p.add_argument("--resume", action="store_true", help="collect: continuar --run desde el último tick")
    p.add_argument("--fresh-ledger", action="store_true",
                   help="evaluate: ledger nuevo en cada tick (mide persistencia/episodios)")
    p.add_argument("--max-rss-mb", type=float, default=1500.0)
    p.add_argument("--max-minutes", type=float, default=None)
    p.add_argument("--ticks", type=int, default=10)
    p.add_argument("--interval-sec", type=float, default=30)
    p.add_argument("--latency-ms", type=float, default=500)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--modules", default=None)
    p.add_argument("--sources", default="crypto,polymarket,dex,futures",
                   help="collect: fuentes a recolectar (crypto,polymarket,dex,futures,ccl)")
    p.add_argument("--run", default=None)
    p.add_argument("--notify", action="store_true")
    p.add_argument("--top", type=int, default=50)
    p.add_argument("--max-events", type=int, default=300)
    p.add_argument("--kalshi-pages", type=int, default=20)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                        format="%(asctime)s %(levelname)s %(message)s")
    {"verify-collect": cmd_verify_collect, "episodes": cmd_episodes, "pm-gaps": cmd_pm_gaps, "consolidate": cmd_consolidate, "research": cmd_research, "run": cmd_run, "collect": cmd_collect, "evaluate": cmd_replay, "replay": cmd_replay,
     "report": cmd_report,
     "suggest-pairs": cmd_suggest_pairs}[args.cmd](args)


if __name__ == "__main__":
    main()
