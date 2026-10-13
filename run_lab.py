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

DB = Path("lab_data") / "lab.sqlite"
ALL = ("cross_exchange", "triangular", "basis_funding", "polymarket_buy_all_no",
       "prediction_cross_venue", "liquidity_provision")
log = logging.getLogger("lab")


def make_modules(names, run_id, seed, live=True):
    from lab.modules.cross_exchange import CrossExchange
    from lab.modules.liquidity import LiquidityProvision
    from lab.modules.prediction import CrossVenuePrediction, PolymarketBuyAllNo
    from lab.modules.triangular import Triangular
    out = []
    for n in names:
        if n == "cross_exchange":
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
    markets = {}
    pairs = next((m.pairs for m in mods if m.name == "prediction_cross_venue"), [])
    kalshi = None
    if pairs:
        from src.kalshi_public import KalshiPublicClient
        kalshi = KalshiPublicClient()
    log.info("pares Kalshi~Polymarket verificados: %d", len(pairs))
    log.info("run %s: módulos %s", run_id, [m.name for m in mods])
    try:
        for t in range(args.ticks):
            t0 = time.monotonic()
            snap = build_snapshot(t, crypto, pm, args.latency_ms, markets_cache=markets,
                                  pairs=pairs, kalshi_client=kalshi)
            store.save_snapshot(run_id, snap)
            counts = lab.run_tick(snap)
            log.info("tick %d: %s | errores de fuentes %d | %.1fs", t, counts, len(snap.errors),
                     time.monotonic() - t0)
            if t < args.ticks - 1:
                time.sleep(max(0.0, args.interval_sec - (time.monotonic() - t0)))
    except KeyboardInterrupt:
        log.info("Cortado por el usuario.")
    finally:
        lab.finish()
    report(store, run_id, args.notify)


def cmd_replay(args):
    store = LabStore(DB)
    src = args.run or store.latest_run("live")
    if not src:
        sys.exit("No hay corridas en vivo guardadas para reproducir.")
    snaps = store.load_snapshots(src)
    run_id = f"replay-{src}-s{args.seed}-{time.strftime('%H%M%S')}"
    store.start_run(run_id, now_iso(), "replay", args.seed, source_run=src, args=vars(args))
    names = args.modules.split(",") if args.modules else ALL
    lab = Lab(make_modules(names, run_id, args.seed, live=False), store, run_id,
              ExecConfig(latency_ms=snaps[0].latency_ms if snaps else 500, seed=args.seed))
    for s in snaps:
        lab.run_tick(s)
    lab.finish()
    log.info("replay de %s: %d ticks", src, len(snaps))
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


def main(argv=None):
    if not PAPER_ONLY:
        sys.exit("El laboratorio es solo simulación (PAPER_ONLY).")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["run", "replay", "report", "suggest-pairs"])
    p.add_argument("--ticks", type=int, default=10)
    p.add_argument("--interval-sec", type=float, default=30)
    p.add_argument("--latency-ms", type=float, default=500)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--modules", default=None)
    p.add_argument("--run", default=None)
    p.add_argument("--notify", action="store_true")
    p.add_argument("--top", type=int, default=50)
    p.add_argument("--max-events", type=int, default=300)
    p.add_argument("--kalshi-pages", type=int, default=20)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                        format="%(asctime)s %(levelname)s %(message)s")
    {"run": cmd_run, "replay": cmd_replay, "report": cmd_report,
     "suggest-pairs": cmd_suggest_pairs}[args.cmd](args)


if __name__ == "__main__":
    main()
