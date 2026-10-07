"""PIE A PIE - funding/basis (spot largo + perp corto, mismo exchange).

SOLO lectura de datos públicos y paper trading. Sin claves, sin órdenes, sin
retiros. Datos de alta frecuencia en funding_data/ (SQLite, fuera de git);
resúmenes en reports/funding_basis/.

  python run_funding.py probe              verifica endpoints públicos (REST)
  python run_funding.py probe-ws           verifica WebSocket (ccxt.pro)
  python run_funding.py phase0             Fase 0: ~90 días históricos
  python run_funding.py live --once        un tick de paper en vivo
  python run_funding.py live               proceso persistente (Ctrl+C corta)
  python run_funding.py report             imprime los resúmenes
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from funding.config import PAPER_ONLY, FundingConfig
from funding.report import REPORT_DIR, live_summary, ntfy_text, phase0_summary

DB_PATH = Path("funding_data") / "funding.sqlite"
log = logging.getLogger("funding")


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def adapters_for(names):
    from funding.adapters import make_adapter
    out = {}
    for n in names:
        try:
            out[n] = make_adapter(n)
        except Exception as e:  # noqa: BLE001 - un exchange caído no corta todo
            log.error("No se pudo crear el adaptador %s: %s", n, e)
    return out


def cmd_probe(cfg, args):
    res = {}
    for name, a in adapters_for(cfg.exchanges).items():
        res[name] = a.probe(args.asset)
        for k, v in res[name].items():
            print(f"{name:8s} {k:16s} {v}")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "endpoint_probe.json").write_text(
        json.dumps({"generated_at": now_iso(), "asset": args.asset, "results": res},
                   indent=1), encoding="utf-8")


def cmd_probe_ws(cfg, args):
    from funding.market_data import WsBooks
    ads = adapters_for(cfg.exchanges)
    ws = WsBooks(ads, [(e, args.asset) for e in ads])
    time.sleep(args.seconds)
    for (ex, asset, kind), n in sorted(ws.updates.items()):
        print(f"{ex:8s} {asset} {kind:4s} actualizaciones WS: {n}")
    for ex in ads:
        for kind in ("spot", "perp"):
            if (ex, args.asset, kind) not in ws.updates:
                print(f"{ex:8s} {args.asset} {kind:4s} SIN DATOS por WS")
    for e in ws.errors[:10]:
        print("error:", e)
    ws.close()


def cmd_phase0(cfg, args):
    from funding.phase0 import analyze_pair
    from funding.storage import Storage
    st = Storage(DB_PATH)
    now_ms = int(time.time() * 1000)
    results = []
    ads = adapters_for(cfg.exchanges)
    for name in cfg.exchanges:
        if name not in ads:
            results += [{"exchange": name, "asset": a, "status": "ADAPTER_ERROR",
                         "errors": ["no se pudo crear el adaptador"]} for a in cfg.assets]
            continue
        for asset in cfg.assets:
            t0 = time.perf_counter()
            try:
                results.append(analyze_pair(ads[name], asset, cfg, st, now_ms, log))
            except Exception as e:  # noqa: BLE001
                log.exception("%s %s falló", name, asset)
                results.append({"exchange": name, "asset": asset, "status": "ERROR",
                                "errors": [f"{type(e).__name__}: {e}"]})
            log.info("  (%s %s en %.1fs)", name, asset, time.perf_counter() - t0)
    from funding.phase0 import sensitivity
    for r in results:
        if r.get("status") == "OK":
            r["sensitivity_by_horizon_days"] = sensitivity(st, r, cfg)
    data = phase0_summary(results, cfg, now_iso())
    st.close()
    print(json.dumps(data["totals"], indent=1))
    print(f"Reporte: {REPORT_DIR / 'phase0_report.md'}")


def cmd_live(cfg, args):
    from funding.live import LiveRunner
    from funding.market_data import RestBooks, WsBooks
    from funding.storage import Storage
    from src.notify import send

    st = Storage(DB_PATH)
    ads = adapters_for(cfg.exchanges)
    books = (WsBooks(ads, [(e, a) for e in ads for a in cfg.assets]) if args.ws
             else RestBooks(ads))
    runner = LiveRunner(cfg, ads, st, books, log, seed=args.seed)
    last_summary = st.get("last_summary_ts", 0)
    ticks = 0
    try:
        while True:
            t0 = time.monotonic()
            closed_before = len(runner.state.ledger.closed)
            open_before = set(runner.state.ledger.open)
            res = runner.tick()
            ticks += 1
            ok = sum(1 for r in res.values() if r.get("ok"))
            pos = sum(1 for r in res.values() if r.get("ok") and r["expected_net_pct"] > 0)
            log.info("tick %d: %d/%d pares ok, %d con neto esperado > 0 | caja US$%.2f, "
                     "bloqueado US$%.2f", ticks, ok, len(res), pos,
                     runner.state.ledger.cash, runner.state.ledger.locked)
            summary = live_summary(st, runner.state.ledger, now_iso())
            topic = os.environ.get("NTFY_TOPIC", "").strip()
            changed = (set(runner.state.ledger.open) != open_before
                       or len(runner.state.ledger.closed) != closed_before)
            due = time.time() - last_summary >= args.summary_hours * 3600
            if topic and (changed or due):   # sin spam: solo cambios paper o resumen
                title, body = ntfy_text(summary)
                send(topic, title, body, 3 if changed else 2, ["chart_with_upwards_trend"])
                last_summary = time.time()
                st.put("last_summary_ts", last_summary)
            if args.once or (args.max_ticks and ticks >= args.max_ticks):
                break
            time.sleep(max(0.0, args.interval_sec - (time.monotonic() - t0)))
    except KeyboardInterrupt:
        log.info("Cortado por el usuario.")
    finally:
        books.close()
        st.put("paper_ledger", runner.state.ledger.to_dict())
        st.close()


def cmd_report(cfg, args):
    for name in ("phase0_summary.json", "live_summary.json"):
        p = REPORT_DIR / name
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            print(f"== {name} ({d.get('generated_at')})")
            print(json.dumps(d.get("totals") or {k: v for k, v in d.items()
                                                  if k not in ("pairs",)}, indent=1))
        else:
            print(f"== {name}: no existe todavía")


def main(argv=None):
    if not PAPER_ONLY:
        sys.exit("paper_only debe ser True: funding/basis es solo paper.")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["probe", "probe-ws", "phase0", "live", "report"])
    p.add_argument("--asset", default="BTC")
    p.add_argument("--seconds", type=float, default=15)
    p.add_argument("--once", action="store_true")
    p.add_argument("--ws", action="store_true", help="libros por WebSocket (ccxt.pro)")
    p.add_argument("--interval-sec", type=float, default=60)
    p.add_argument("--max-ticks", type=int, default=0)
    p.add_argument("--summary-hours", type=float, default=12)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--exchanges", default=None)
    p.add_argument("--assets", default=None)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                        format="%(asctime)s %(levelname)s %(message)s")
    cfg = FundingConfig()
    if args.exchanges:
        cfg = FundingConfig(**{**cfg.__dict__, "exchanges": tuple(args.exchanges.split(","))})
    if args.assets:
        cfg = FundingConfig(**{**cfg.__dict__, "assets": tuple(args.assets.split(","))})
    {"probe": cmd_probe, "probe-ws": cmd_probe_ws, "phase0": cmd_phase0,
     "live": cmd_live, "report": cmd_report}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
