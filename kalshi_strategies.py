"""PIE A PIE - estrategias Kalshi experimentales (solo lectura / paper trading).

Corre un ciclo de buy_all_no y strike_inconsistency. Cada estrategia tiene su
propio capital, posiciones, P&L y rachas en data/strategies/<estrategia>/.
kalshi_current (scanner.py) no se toca ni comparte estado con estas.

  python kalshi_strategies.py --interval-min 25
"""

import argparse
import logging
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from src.config import BotConfig, ScannerConfig
from src.kalshi_public import KalshiPublicClient
from src.strategies import buy_all_no, strike_inconsistency
from src.strategies.kalshi_common import (
    DISCARD_FIELDS, OPPORTUNITY_FIELDS, STRATEGY_CYCLE_FIELDS, StrategyStore,
    expected_close, fetch_books, is_net_positive, open_paper, opportunity_row, settle_open_positions,
)
from src.tracking import DURATION_FIELDS

log = logging.getLogger("kalshi_strategies")
ROOT = Path("data") / "strategies"
NEAR_MISS_MAX_COST_RATIO = 1.03   # costo/pago mínimo < 1.03, como kalshi_current


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_candidates(strategy, events, args):
    reasons, cands = Counter(), []
    for ev in events:
        if strategy == buy_all_no.STRATEGY:
            c, why = buy_all_no.prefilter(ev, min_volume_24h=args.min_volume,
                                          slippage=args.slippage)
            reasons[why] += 1
            if c:
                cands.append(c)
        else:
            cs, why = strike_inconsistency.candidates_for_event(
                ev, min_volume_24h=args.min_volume)
            reasons.update(why)
            cands.extend(cs)
    cands.sort(key=lambda c: -c["gross_top"])
    if len(cands) > args.max_candidates:
        reasons["OVER_CANDIDATE_CAP"] += len(cands) - args.max_candidates
    reasons.pop("OK", None)
    return cands[:args.max_candidates], reasons


def tickers_of(strategy, cand):
    if strategy == buy_all_no.STRATEGY:
        return [m["ticker"] for m in cand["legs"]]
    return [cand["broad"]["ticker"], cand["narrow"]["ticker"]]


def evaluate(strategy, cand, books, budget, bot, args):
    kw = dict(slippage=args.slippage, min_net_edge=bot.min_net_edge, budget_usd=budget)
    if strategy == buy_all_no.STRATEGY:
        return buy_all_no.evaluate(cand, books, **kw)
    return strike_inconsistency.evaluate(cand, books, **kw)


def run_strategy(strategy, client, events, args, bot, ts):
    t0 = time.perf_counter()
    store = StrategyStore(ROOT, strategy, bot.starting_capital_usd,
                          max_gap_min=args.interval_min * 1.5)
    row = {"timestamp": ts, "strategy": strategy, "ok": 1, "events_seen": len(events)}
    row["paper_settled"] = settle_open_positions(client, store, ts, log)

    cands, reasons = build_candidates(strategy, events, args)
    row["candidates"] = len(cands)

    t_books = time.perf_counter()
    budget = store.book.cash * bot.max_capital_per_trade
    results, timeouts, errors = [], 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(fetch_books, client, tickers_of(strategy, c),
                            args.event_timeout): c for c in cands}
        for fut in as_completed(futs):
            c = futs[fut]
            try:
                books = fut.result()
            except TimeoutError:
                timeouts += 1
                reasons["TIMEOUT"] += 1
                continue
            except Exception as e:  # noqa: BLE001 - un evento no corta el ciclo
                errors += 1
                reasons["BOOK_ERROR"] += 1
                log.warning("    [%s] error de libro: %s", strategy, e)
                continue
            results.append((c, evaluate(strategy, c, books, budget, bot, args)))
    row.update(evaluated=len(results), timeouts=timeouts, errors=errors,
               t_books_s=round(time.perf_counter() - t_books, 2))

    opps = net_pos = exe = opened = 0
    for c, r in results:
        if r.reason != "NET_EDGE_OK":
            reasons[r.reason] += 1
        near = (r.min_payout_per_bundle > 0 and r.best_bundle_cost
                < NEAR_MISS_MAX_COST_RATIO * r.min_payout_per_bundle)
        if not near:
            continue
        opps += 1
        net_pos += is_net_positive(r)
        store.log("opportunities.csv", OPPORTUNITY_FIELDS, opportunity_row(ts, r))
        if not r.executable:
            continue
        exe += 1
        legs = c["legs"] if strategy == buy_all_no.STRATEGY else [c["broad"], c["narrow"]]
        pos, why = open_paper(store, r, expected_close(legs), ts)
        opened += pos is not None
        log.info("    [%s] EJECUTABLE %s: %d contratos, neto US$%+.2f -> paper %s",
                 strategy, r.key, r.contracts, r.net_profit, why)

    exe_keys = {r.key for _, r in results if r.executable}
    for streak in store.tracker.update(ts, exe_keys, {r.key for _, r in results}):
        store.log("durations.csv", DURATION_FIELDS, streak)
    for reason, count in sorted(reasons.items()):
        store.log("discards.csv", DISCARD_FIELDS,
                  {"timestamp": ts, "strategy": strategy, "reason": reason, "count": count})

    row.update(opportunities=opps, net_positive=net_pos, executable=exe,
               paper_opened=opened, t_total_s=round(time.perf_counter() - t0, 2))
    store.save()
    store.log("cycles.csv", STRATEGY_CYCLE_FIELDS, row)
    log.info("[%s] candidatos %d, evaluados %d, oportunidades %d, net-positive %d, "
             "ejecutables %d | caja US$%.2f, bloqueado US$%.2f | %.1fs",
             strategy, len(cands), len(results), opps, net_pos, exe,
             store.book.cash, store.book.locked, row["t_total_s"])
    return row


def main(argv=None):
    bot, scfg = BotConfig(), ScannerConfig()
    if not bot.paper_only:
        sys.exit("BotConfig.paper_only debe ser True: solo paper trading.")
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--interval-min", type=float, default=25.0)
    p.add_argument("--strategies", default="buy_all_no,strike_inconsistency")
    p.add_argument("--min-volume", type=float, default=scfg.min_event_volume_24h)
    p.add_argument("--slippage", type=float, default=bot.estimated_slippage)
    p.add_argument("--max-candidates", type=int, default=150)
    p.add_argument("--event-timeout", type=float, default=scfg.event_timeout_s)
    p.add_argument("--workers", type=int, default=scfg.max_workers)
    p.add_argument("--max-pages", type=int, default=None)
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                        format="%(asctime)s %(levelname)s %(message)s")

    client = KalshiPublicClient(
        timeout=scfg.request_timeout_s, tokens_per_second=scfg.read_tokens_per_second,
        tokens_per_read=scfg.tokens_per_read, max_retries=scfg.max_retries,
        pool_size=args.workers * 2)
    ts = now_iso()
    failed = []
    try:
        t0 = time.perf_counter()
        events = list(client.iter_events(status="open", with_nested_markets=True,
                                         limit=scfg.events_page_size,
                                         max_pages=args.max_pages))
        log.info("Eventos abiertos: %d en %.1fs", len(events), time.perf_counter() - t0)
    except Exception as e:  # noqa: BLE001
        events, listing_error = None, e
    for strategy in [s.strip() for s in args.strategies.split(",") if s.strip()]:
        try:
            if events is None:
                raise listing_error
            run_strategy(strategy, client, events, args, bot, ts)
        except Exception as e:  # noqa: BLE001 - una estrategia no tumba a la otra
            failed.append(strategy)
            log.exception("[%s] ciclo fallido", strategy)
            StrategyStore(ROOT, strategy, bot.starting_capital_usd, 1).log(
                "cycles.csv", STRATEGY_CYCLE_FIELDS,
                {"timestamp": ts, "strategy": strategy, "ok": 0, "error": repr(e)[:200]})
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
