"""PIE A PIE - ejecutor de órdenes de HORUS (modo 2). SOLO paper.

  python run_executor.py example > orden.json         orden de ejemplo (horus.order/v1)
  python run_executor.py process [--loop --every 15]   procesa el buzón y avanza las órdenes
  python run_executor.py status [ORDER_ID]             estado y reporte
  python run_executor.py verify                        verifica la cadena de eventos

Buzón: executor_io/inbox/*.json (órdenes y cancelaciones) -> procesados en
executor_io/inbox/processed/; reportes en executor_io/outbox/. Estado en
lab_data/executor.sqlite. Libros públicos sin claves (ccxt). No envía órdenes
reales ni escribe en data/.
"""

import argparse
import json
import logging
import sys
import time
from datetime import timedelta
from pathlib import Path

from executor import PAPER_ONLY
from executor.engine import Engine
from executor.limits import load_limits
from executor.schema import now_utc
from executor.store import ExecutorStore

IO = Path("executor_io")
DB = Path("lab_data") / "executor.sqlite"
log = logging.getLogger("executor")


def live_books_fn():
    """Libros públicos (ccxt, sin claves) de los venues pedidos."""
    from lab.sources import CryptoSource
    cache = {}

    def fn(symbol, venues):
        missing = [v for v in venues if v not in cache]
        if missing:
            cache.update(CryptoSource(venues=tuple(missing)).ex)
        src = CryptoSource(exchanges={v: cache[v] for v in venues if v in cache})
        books, errs = src.fetch_books(symbols=(symbol,), depth=20)
        return {k.split("|")[0]: b for k, b in books.items()}, errs
    return fn


def engine(books_fn=None):
    return Engine(ExecutorStore(DB), load_limits(), books_fn or live_books_fn(),
                  outbox=IO / "outbox")


def process_inbox(eng, inbox=IO / "inbox"):
    done = inbox / "processed"
    done.mkdir(parents=True, exist_ok=True)
    out = []
    for f in sorted(inbox.glob("*.json")):
        try:
            msg = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            msg = {"_invalid_json": str(e)}
        rep = eng.process_message(msg)
        out.append(rep)
        log.info("%s -> %s %s", f.name, rep.get("state"), rep.get("reason_code"))
        f.rename(done / f"{int(time.time() * 1000)}-{f.name}")
    return out


def cmd_example(args):
    now = now_utc()
    print(json.dumps({
        "schema": "horus.order/v1", "order_id": f"ex-{now.strftime('%Y%m%d%H%M%S')}",
        "issuer": "horus", "issued_at": now.isoformat(),
        "valid_until": (now + timedelta(hours=2)).isoformat(), "mode": "paper",
        "strategy": {"name": "ejemplo_ruptura", "version": "0.1.0"},
        "instrument": {"asset_class": "crypto_spot", "symbol": "ETH/USDT",
                       "venues_allowed": ["binance", "bybit", "okx"]},
        "direction": "buy", "sizing": {"notional_usd": 20.0},
        "entry": {"type": "market", "max_slippage_bps": 15, "max_wait_s": 120, "allow_partial": False},
        "exit": {"take_profit": 999999.0, "stop": 1.0},
        "risk": {"max_loss_usd": 20.0}, "on_problem": "halt_and_report",
        "_nota": "ajustar stop/take_profit al precio real; el stop define la pérdida máxima"},
        indent=1))


def cmd_process(args):
    eng = engine()
    while True:
        process_inbox(eng)
        eng.step()
        if not args.loop:
            break
        time.sleep(args.every)


def cmd_status(args):
    store = ExecutorStore(DB)
    eng = Engine(store, load_limits(), lambda s, v: ({}, []))
    if args.order_id:
        print(json.dumps({"report": eng.report(args.order_id), "events": store.events(args.order_id)},
                         indent=1, default=str, ensure_ascii=False))
        return
    for o in store.orders():
        print(o["order_id"], o["state"], o["payload"]["strategy"]["name"])
    print("ledger:", json.dumps(eng.ledger.st))


def cmd_verify(args):
    ok = ExecutorStore(DB).verify_chain()
    print("cadena de eventos íntegra" if ok else "CADENA ALTERADA")
    sys.exit(0 if ok else 1)


def main(argv=None):
    if not PAPER_ONLY:
        sys.exit("El ejecutor es solo paper.")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["example", "process", "status", "verify"])
    p.add_argument("order_id", nargs="?")
    p.add_argument("--loop", action="store_true")
    p.add_argument("--every", type=float, default=15.0)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    {"example": cmd_example, "process": cmd_process, "status": cmd_status, "verify": cmd_verify}[args.cmd](args)


if __name__ == "__main__":
    main()
