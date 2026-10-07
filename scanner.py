"""PIE A PIE - scanner de arbitraje intra-evento (solo lectura / paper trading).

Busca eventos mutuamente excluyentes y exhaustivos donde comprar YES en todos
los resultados cueste menos de 1.00 USD neto de comisiones y slippage.
No envía órdenes ni usa credenciales.

  python scanner.py                          un ciclo
  python scanner.py --loop --interval-min 10 ciclos hasta Ctrl+C
  python scanner.py --report                 resumen de lo registrado
"""

import argparse
import logging
import math
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.config import BotConfig, ScannerConfig
from src.event_arbitrage import (
    Prefiltered,
    evaluate_event_bundle,
    prefilter_event,
    yes_asks_from_orderbook,
)
from src.kalshi_public import KalshiPublicClient
from src.paper_trader import PaperBook
from src.report import build_report
from src.tracking import (
    CYCLE_FIELDS, DURATION_FIELDS, NEAR_MISS_FIELDS, PAPER_FIELDS,
    StreakTracker, append_csv, load_json, save_json,
)

log = logging.getLogger("scanner")

DATA = Path("data")
CACHE_FILE = DATA / "events_cache.json"
STATE_FILE = DATA / "state.json"
NEAR_MISS_MAX_SUM = 1.03


class EventTimeout(Exception):
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def fetch_ladders(client, pre, timeout_s, request_timeout_s):
    """Pide el orderbook de cada pata respetando un deadline por evento."""
    deadline = time.monotonic() + timeout_s
    ladders = []
    for m in pre.legs:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise EventTimeout(pre.event_ticker)
        data = client.get_orderbook(
            m["ticker"], timeout=min(request_timeout_s, remaining)
        )
        ladders.append(yes_asks_from_orderbook(data))
    if time.monotonic() > deadline:
        raise EventTimeout(pre.event_ticker)
    return ladders


# ---------------------------------------------------------------- caché ---

def load_cache(args):
    """Eventos filtrados si la caché es reciente y de la misma configuración."""
    c = load_json(CACHE_FILE)
    if not c or c.get("params") != cache_params(args):
        return None
    age = (datetime.now(timezone.utc) - parse_ts(c["refreshed_at"])).total_seconds()
    if age > args.cache_min * 60:
        return None
    return [Prefiltered(**e) for e in c["events"]]


def cache_params(args):
    return {"min_volume": args.min_volume, "gap_tol": args.gap_tol}


def refresh_cache(client, args, scfg):
    """Lista eventos abiertos y guarda los que pasan el filtro estructural."""
    t0 = time.perf_counter()
    events = list(client.iter_events(
        status="open", with_nested_markets=True,
        limit=scfg.events_page_size, max_pages=args.max_pages,
    ))
    reasons, kept = Counter(), []
    for ev in events:
        pre, reason = prefilter_event(
            ev, min_volume_24h=args.min_volume, gap_tol=args.gap_tol,
            check_prices=False,
        )
        reasons[reason] += 1
        if pre:
            kept.append(pre)
    save_json(CACHE_FILE, {"refreshed_at": now_iso(), "params": cache_params(args),
                           "events": [asdict(p) for p in kept]})
    log.info("Caché: %d eventos listados -> %d estructuralmente válidos en %.2fs",
             len(events), len(kept), time.perf_counter() - t0)
    for reason, count in reasons.most_common():
        log.info("    %-28s %d", reason, count)
    return kept


def get_candidates(client, args, scfg):
    """Devuelve (eventos, refrescada?, segundos). Con error de red usa la vieja."""
    cached = load_cache(args)
    if cached is not None:
        return cached, False, 0.0
    t0 = time.perf_counter()
    try:
        return refresh_cache(client, args, scfg), True, time.perf_counter() - t0
    except Exception as e:  # noqa: BLE001
        old = load_json(CACHE_FILE)
        if old and old.get("params") == cache_params(args):
            log.warning("No se pudo refrescar la caché (%s); uso la de %s",
                        e, old["refreshed_at"])
            return ([Prefiltered(**x) for x in old["events"]], False,
                    time.perf_counter() - t0)
        raise


# ---------------------------------------------------------------- ciclo ---

def expected_close(pre):
    times = [parse_ts(m.get("expected_expiration_time") or m.get("close_time"))
             for m in pre.legs]
    times = [t for t in times if t]
    return max(times).isoformat() if times else None


def any_leg_closed(pre, now_dt):
    return any((t := parse_ts(m.get("close_time"))) and t <= now_dt
               for m in pre.legs)


def settle_positions(client, book, ts):
    settled = 0
    for pos in list(book.open):
        try:
            data = client.get(f"events/{pos.event_ticker}",
                              params={"with_nested_markets": "true"})
        except Exception as e:  # noqa: BLE001
            log.warning("    no se pudo consultar %s: %s", pos.event_ticker, e)
            continue
        markets = (data.get("event") or {}).get("markets") or data.get("markets") or []
        if book.try_settle(pos, {m.get("ticker"): m for m in markets}, ts):
            settled += 1
            log.info("    PAPER cerrada %s: pago US$%.2f, neto US$%+.2f",
                     pos.event_ticker, pos.payout, pos.realized_net)
            append_csv(DATA / "paper_trades.csv", PAPER_FIELDS, {
                "timestamp": ts, "action": "SETTLE",
                "event_ticker": pos.event_ticker, "contracts": pos.contracts,
                "cost": pos.cost, "fees": pos.fees, "slippage": pos.slippage,
                "expected_net": pos.expected_net,
                "expected_close": pos.expected_close, "payout": pos.payout,
                "realized_net": pos.realized_net, "cash_after": book.cash,
            })
    return settled


def run_cycle(client, args, bot, scfg, book, tracker):
    t_cycle = time.perf_counter()
    ts = now_iso()
    now_dt = parse_ts(ts)
    row = {"timestamp": ts, "ok": 1}

    # 1) Eventos filtrados (caché de --cache-min minutos).
    candidates, refreshed, t_list = get_candidates(client, args, scfg)
    row.update(cache_refreshed=int(refreshed), t_list_s=round(t_list, 2))

    # 2) Liquidar posiciones paper cuyos mercados ya resolvieron.
    row["paper_settled"] = settle_positions(client, book, ts)

    # 3) Seleccionar: patas aún abiertas, ranking por suma de ask cacheada.
    live = [p for p in candidates if not any_leg_closed(p, now_dt)]
    live.sort(key=lambda c: c.prelim_sum)
    selected = live[:args.max_events]
    row["candidates"] = len(live)
    log.info("Ciclo %s: %d candidatos (%d con patas ya cerradas), %d a evaluar",
             ts, len(live), len(candidates) - len(live), len(selected))

    # 4) Orderbooks con concurrencia limitada (el TokenBucket marca el ritmo).
    t0 = time.perf_counter()
    budget = book.cash * bot.max_capital_per_trade
    results, timeouts, errors = [], 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch_ladders, client, p, args.event_timeout,
                               scfg.request_timeout_s): p for p in selected}
        for fut in as_completed(futures):
            pre = futures[fut]
            try:
                ladders = fut.result()
            except EventTimeout:
                timeouts += 1
                log.warning("    %s: timeout (> %.1fs)", pre.event_ticker,
                            args.event_timeout)
                continue
            except Exception as e:  # noqa: BLE001 - un evento no corta el ciclo
                errors += 1
                log.warning("    %s: error %s", pre.event_ticker, e)
                continue
            results.append((pre, evaluate_event_bundle(
                pre, ladders,
                fee_coefficient=bot.taker_fee_coefficient,
                slippage_per_contract=bot.estimated_slippage,
                min_net_edge=bot.min_net_edge,
                budget_usd=budget,
                min_sane_ask_sum=scfg.min_sane_ask_sum,
            )))
    row.update(evaluated=len(results), timeouts=timeouts, errors=errors,
               t_books_s=round(time.perf_counter() - t0, 2))

    # 5) Casi-aciertos, rachas y paper.
    near = executable = opened = 0
    for pre, o in results:
        if not o.best_ask_sum < NEAR_MISS_MAX_SUM:
            continue
        near += 1
        reference = o.reason == "NO_POSITIVE_MARGINAL_EDGE"
        append_csv(DATA / "near_misses.csv", NEAR_MISS_FIELDS, {
            "timestamp": ts, "event_ticker": o.event_ticker,
            "ask_sum": round(o.best_ask_sum, 4), "n_legs": o.n_legs,
            "contracts_evaluated": o.contracts or int(reference),
            "est_fees": round(o.estimated_fees, 4),
            "est_net": round(o.net_profit_per_contract if reference
                             else o.net_profit, 4),
            "depth_top": min(size for _, _, size in o.legs),
            "depth_with_edge": o.max_contracts_available,
            "executable": o.executable, "reason": o.reason,
        })
        if not o.executable:
            continue
        executable += 1
        pos, why = book.try_open(o, expected_close(pre), ts)
        log.info("    EJECUTABLE %s: %d contratos, neto US$%+.2f -> paper %s",
                 o.event_ticker, o.contracts, o.net_profit, why)
        if pos:
            opened += 1
            append_csv(DATA / "paper_trades.csv", PAPER_FIELDS, {
                "timestamp": ts, "action": "OPEN",
                "event_ticker": pos.event_ticker, "contracts": pos.contracts,
                "cost": pos.cost, "fees": pos.fees, "slippage": pos.slippage,
                "expected_net": pos.expected_net,
                "expected_close": pos.expected_close, "cash_after": book.cash,
            })

    exe_set = {o.event_ticker for _, o in results if o.executable}
    for streak in tracker.update(ts, exe_set, {o.event_ticker for _, o in results}):
        append_csv(DATA / "opportunity_durations.csv", DURATION_FIELDS, streak)

    row.update(near_misses=near, executable=executable, paper_opened=opened,
               t_total_s=round(time.perf_counter() - t_cycle, 2))
    save_state(book, tracker)
    append_csv(DATA / "cycles.csv", CYCLE_FIELDS, row)
    log.info("Ciclo listo: %d evaluados, %d casi-aciertos, %d ejecutables, "
             "%d paper abiertas, %d liquidadas | libros %.2fs, total %.2fs",
             len(results), near, executable, opened, row["paper_settled"],
             row["t_books_s"], row["t_total_s"])
    print_top(results, args.top, book)


def print_top(results, top, book):
    results = sorted((o for _, o in results),
                     key=lambda o: (not o.executable,
                                    o.best_ask_sum if not math.isnan(o.best_ask_sum)
                                    else math.inf))
    for i, o in enumerate(results[:top], 1):
        flag = "ARB" if o.executable else "---"
        print(f"  {i:02d} [{flag}] {o.event_ticker} | patas={o.n_legs} | "
              f"suma_ask={o.best_ask_sum:.4f} | neto/contrato="
              f"{o.net_profit_per_contract:+.4f} | {o.reason}")
    print(f"  paper: caja US${book.cash:.2f} | bloqueado US${book.locked:.2f} "
          f"| neto realizado US${book.realized_net:+.2f}")


def save_state(book, tracker):
    save_json(STATE_FILE, {"paper": book.to_dict(), "streaks": tracker.active})


# ----------------------------------------------------------------- main ---

def parse_args(scfg):
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--loop", action="store_true", help="repetir hasta Ctrl+C")
    p.add_argument("--interval-min", type=float, default=10.0)
    p.add_argument("--report", action="store_true", help="imprimir resumen y salir")
    p.add_argument("--cache-min", type=float, default=scfg.cache_refresh_min)
    p.add_argument("--max-events", type=int, default=scfg.max_events_per_run)
    p.add_argument("--event-timeout", type=float, default=scfg.event_timeout_s)
    p.add_argument("--min-volume", type=float, default=scfg.min_event_volume_24h)
    p.add_argument("--max-pages", type=int, default=None,
                   help="tope de páginas de GET /events (default: todas)")
    p.add_argument("--gap-tol", type=float, default=0.0,
                   help="hueco tolerado entre rangos de strikes (default 0: apagado)")
    p.add_argument("--workers", type=int, default=scfg.max_workers)
    p.add_argument("--top", type=int, default=10)
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args()


def main():
    bot, scfg = BotConfig(), ScannerConfig()
    if not bot.paper_only:
        sys.exit("BotConfig.paper_only debe ser True: este scanner es solo paper.")
    args = parse_args(scfg)

    if args.report:
        print(build_report(DATA, bot.starting_capital_usd, args.interval_min))
        return

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    client = KalshiPublicClient(
        timeout=scfg.request_timeout_s,
        tokens_per_second=scfg.read_tokens_per_second,
        tokens_per_read=scfg.tokens_per_read,
        max_retries=scfg.max_retries,
        pool_size=args.workers * 2,
    )
    state = load_json(STATE_FILE, {}) or {}
    book = PaperBook.from_dict(state.get("paper"), bot.starting_capital_usd)
    tracker = StreakTracker(state.get("streaks"),
                            max_gap_min=args.interval_min * 1.5)

    try:
        while True:
            started = time.monotonic()
            try:
                run_cycle(client, args, bot, scfg, book, tracker)
            except Exception as e:  # noqa: BLE001 - el loop no se cae
                append_csv(DATA / "cycles.csv", CYCLE_FIELDS,
                           {"timestamp": now_iso(), "ok": 0, "error": repr(e)[:200]})
                if not args.loop:
                    raise  # en un solo ciclo (Actions) queda registrado y falla
                log.exception("Ciclo fallido; sigo en el próximo")
            if not args.loop:
                return
            wait = args.interval_min * 60 - (time.monotonic() - started)
            log.info("Próximo ciclo en %.0fs (Ctrl+C para cortar)", max(wait, 0))
            time.sleep(max(wait, 0))
    except KeyboardInterrupt:
        save_state(book, tracker)
        log.info("Cortado por el usuario. Estado guardado en %s", STATE_FILE)


if __name__ == "__main__":
    main()
