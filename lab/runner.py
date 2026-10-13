"""Orquestación del laboratorio: un snapshot compartido por tick, evaluación de
módulos en paralelo y ejecución simulada en orden fijo (reclamos de liquidez
deterministas). Errores aislados por módulo; nada se inventa."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from . import PAPER_ONLY
from .core import ExecConfig, LiquidityRegistry, StrategyLedger, classify_lab
from .modules.base import Context
from .sources import CRYPTO_SYMBOLS, MM_MARKETS, Snapshot, now_iso

log = logging.getLogger("lab")

EXEC_ORDER = ("cross_exchange", "triangular", "polymarket_buy_all_no",
              "prediction_cross_venue", "liquidity_provision", "basis_funding")


def fetch_kalshi_quotes(client, tickers):
    """YES/NO ask de Kalshi desde el libro (solo bids: ask = 1 - bid contrario)."""
    from src.strategies.kalshi_common import asks_for, parse_book
    out, errs = {}, []
    for t in tickers:
        try:
            b = parse_book(client.get_orderbook(t))
            ya, na = asks_for(b, "yes"), asks_for(b, "no")
            out[t] = {"yes_ask": ya[0][0] if ya else None, "no_ask": na[0][0] if na else None,
                      "yes_asks": ya, "no_asks": na}
        except Exception as e:  # noqa: BLE001
            errs.append({"venue": "kalshi", "what": "orderbook", "ticker": t,
                         "error": f"{type(e).__name__}: {str(e)[:120]}"})
    return out, errs


def build_snapshot(tick, crypto=None, polymarket=None, latency_ms=500.0, need_trades=True,
                   need_polymarket=True, sleep=time.sleep, markets_cache=None,
                   pairs=None, kalshi_client=None):
    snap = Snapshot(tick=tick, ts=now_iso(), latency_ms=latency_ms)
    if crypto is not None:
        snap.errors.extend(crypto.init_errors)
        snap.books, errs = crypto.fetch_books(CRYPTO_SYMBOLS)
        snap.errors.extend(errs)
        if markets_cache is not None:
            for k in snap.books:
                if k not in markets_cache:
                    v, s = k.split("|")
                    try:
                        markets_cache[k] = crypto.market_meta(v, s)
                    except Exception as e:  # noqa: BLE001
                        snap.errors.append({"venue": v, "symbol": s, "what": "market_meta",
                                            "error": str(e)[:120]})
            snap.markets = dict(markets_cache)
    tokens = []
    if polymarket is not None and need_polymarket:
        from .modules.prediction import select_tokens
        pm, errs = polymarket.fetch()
        snap.errors.extend(errs)
        tokens = select_tokens(pm["events"])
        for p in pairs or []:
            tokens += [p["polymarket_yes_token"], p["polymarket_no_token"]]
        pm["books"], errs = polymarket.fetch_books(tokens)
        snap.errors.extend(errs)
        snap.polymarket = pm
    if pairs and kalshi_client is not None:
        snap.kalshi, errs = fetch_kalshi_quotes(kalshi_client, [p["kalshi_ticker"] for p in pairs])
        snap.errors.extend(errs)
    # Latencia: los libros de ejecución se piden DESPUÉS de esperar.
    sleep(latency_ms / 1000)
    if crypto is not None:
        snap.books_after, errs = crypto.fetch_books(CRYPTO_SYMBOLS)
        snap.errors.extend({**e, "phase": "after_latency"} for e in errs)
        if need_trades:
            snap.trades, errs = crypto.fetch_trades(MM_MARKETS)
            snap.errors.extend(errs)
    if polymarket is not None and need_polymarket and tokens:
        snap.polymarket["books_after"], errs = polymarket.fetch_books(tokens)
        snap.errors.extend({**e, "phase": "after_latency"} for e in errs)
    return snap


class Lab:
    def __init__(self, modules: List, store, run_id, exec_cfg: ExecConfig, capital=100.0):
        assert PAPER_ONLY
        self.modules = {m.name: m for m in modules}
        self.store, self.run_id, self.exec_cfg = store, run_id, exec_cfg
        self.ledgers: Dict[str, StrategyLedger] = {
            n: StrategyLedger(n, capital) for n in self.modules}
        self.last_snap = None
        self.counter = 0

    def _ctx(self, name, registry):
        return Context(exec_cfg=self.exec_cfg, registry=registry,
                       ledger=self.ledgers[name], seed=self.exec_cfg.seed)

    def run_tick(self, snap: Snapshot):
        registry = LiquidityRegistry()
        results, timings = {}, {}

        def evaluate(name):
            t0 = time.perf_counter()
            try:
                return name, self.modules[name].evaluate(snap, self._ctx(name, registry)), None, \
                    time.perf_counter() - t0
            except Exception as e:  # noqa: BLE001 - un módulo no tumba al resto
                log.exception("[%s] evaluate falló", name)
                return name, [], f"{type(e).__name__}: {str(e)[:200]}", time.perf_counter() - t0

        with ThreadPoolExecutor(max_workers=len(self.modules)) as pool:
            for name, opps, err, secs in pool.map(evaluate, list(self.modules)):
                results[name] = (opps, err)
                timings[name] = secs

        for name in sorted(self.modules, key=lambda n: EXEC_ORDER.index(n)
                           if n in EXEC_ORDER else 99):
            opps, err = results[name]
            ctx = self._ctx(name, registry)
            for o in opps:
                try:
                    self.modules[name].execute(o, snap, ctx)
                except Exception as e:  # noqa: BLE001
                    o.reason = f"EXECUTE_ERROR: {type(e).__name__}"
                    log.exception("[%s] execute falló", name)
                o.classification, o.classification_reason = classify_lab(
                    o, getattr(self.modules[name], "nature", "arbitrage"))
                self.counter += 1
                o.uid = f"{self.run_id}:{snap.tick}:{name}:{self.counter}"
                self.store.save_opportunity(self.run_id, o)
            upd = getattr(self.modules[name], "pop_updated", None)
            for o in (upd() if upd else []):
                o.classification, o.classification_reason = classify_lab(
                    o, getattr(self.modules[name], "nature", "arbitrage"))
                self.store.save_opportunity(self.run_id, o)
            self.store.log_tick(self.run_id, snap.tick, snap.ts, name, timings[name],
                                len(opps), err)
        self.store.log_errors(self.run_id, snap.tick, snap.errors)
        self.store.commit()
        self.last_snap = snap
        return {n: len(r[0]) for n, r in results.items()}

    def finish(self):
        for name, m in self.modules.items():
            fin = getattr(m, "finalize", None)
            if fin and self.last_snap is not None:
                fin(self._ctx(name, LiquidityRegistry()), self.last_snap)
            upd = getattr(m, "pop_updated", None)
            for o in (upd() if upd else []):
                self.store.save_opportunity(self.run_id, o)
            summary = self.ledgers[name].summary()
            extra = getattr(m, "ledger_summary", None)
            if extra:
                summary["module_ledger"] = extra()
            self.store.save_ledger(self.run_id, name, summary)
            m.close()
        self.store.commit()
