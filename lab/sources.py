"""Fuentes públicas del laboratorio (solo lectura, sin claves).

Un tick = un Snapshot compartido por todos los módulos:
  books        libros en T0 (detección)
  books_after  libros en T0 + latencia (ejecución simulada)
  trades       trades públicos desde el tick anterior (provisión de liquidez)
  polymarket   eventos negRisk + libros CLOB de los candidatos
  errors       todo lo que falló; los datos faltantes NO se inventan
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests

from . import PAPER_ONLY

CRYPTO_VENUES = ("binance", "bybit", "okx", "kraken", "coinbase")
CRYPTO_SYMBOLS = ("BTC/USDT", "ETH/USDT", "SOL/USDT", "ETH/BTC", "SOL/BTC", "SOL/ETH",
                  "XRP/USDT", "XRP/BTC", "XRP/ETH", "BNB/USDT", "BNB/BTC", "BNB/ETH",
                  "SOL/BNB", "XRP/BNB", "SOL/USDC", "USDC/USDT")
MM_MARKETS = (("binance", "BTC/USDT"), ("okx", "ETH/USDT"), ("bybit", "SOL/USDT"))

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


@dataclass
class Snapshot:
    tick: int
    ts: str
    books: Dict[str, dict] = field(default_factory=dict)        # "venue|symbol" -> book
    books_after: Dict[str, dict] = field(default_factory=dict)
    trades: Dict[str, list] = field(default_factory=dict)
    markets: Dict[str, dict] = field(default_factory=dict)      # metadatos (mínimos, fees ref)
    polymarket: dict = field(default_factory=dict)
    kalshi: dict = field(default_factory=dict)
    dex: dict = field(default_factory=dict)            # Jupiter: quotes T0/T1 + fee de prioridad
    futures: dict = field(default_factory=dict)        # futuros con vencimiento: libros T0/T1
    errors: List[dict] = field(default_factory=list)
    latency_ms: float = 0.0

    @staticmethod
    def k(venue, symbol):
        return f"{venue}|{symbol}"

    def book(self, venue, symbol, after=False):
        return (self.books_after if after else self.books).get(self.k(venue, symbol))

    def to_json(self):
        return json.dumps({k: getattr(self, k) for k in (
            "tick", "ts", "books", "books_after", "trades", "markets", "polymarket",
            "kalshi", "dex", "futures", "errors", "latency_ms")}, default=str)

    @classmethod
    def from_json(cls, s):
        return cls(**json.loads(s))


class CryptoSource:
    """ccxt público. Rechaza claves: el laboratorio nunca opera."""

    def __init__(self, venues=CRYPTO_VENUES, exchanges=None):
        self.ex = {}
        self.init_errors = []
        if exchanges is not None:
            self.ex = exchanges
        else:
            import ccxt
            for v in venues:
                try:
                    e = getattr(ccxt, v)({"enableRateLimit": True, "timeout": 15000})
                    e.load_markets()
                    self.ex[v] = e
                except Exception as err:  # noqa: BLE001
                    self.init_errors.append({"venue": v, "what": "load_markets",
                                             "error": f"{type(err).__name__}: {str(err)[:150]}"})
        for e in self.ex.values():
            assert not getattr(e, "apiKey", None), "no se admiten claves"
        self.last_trade_ms: Dict[str, int] = {}

    def listed(self, venue, symbol):
        return symbol in (getattr(self.ex.get(venue), "markets", None) or {})

    def market_meta(self, venue, symbol):
        m = self.ex[venue].market(symbol)
        lim = m.get("limits") or {}
        return {"min_amount": (lim.get("amount") or {}).get("min"),
                "min_cost": (lim.get("cost") or {}).get("min"),
                "taker_ref": m.get("taker"), "maker_ref": m.get("maker")}

    def _fetch_venue_books(self, venue, symbols, depth):
        out, errs = {}, []
        for s in symbols:
            if not self.listed(venue, s):
                continue
            t = time.perf_counter()
            try:
                ob = self.ex[venue].fetch_order_book(s, depth)
                out[Snapshot.k(venue, s)] = {
                    "bids": [[float(p), float(q)] for p, q, *_ in ob["bids"][:depth]],
                    "asks": [[float(p), float(q)] for p, q, *_ in ob["asks"][:depth]],
                    "fetched_at": now_iso(), "exchange_ts": ob.get("timestamp"),
                    "fetch_ms": round(1000 * (time.perf_counter() - t))}
            except Exception as e:  # noqa: BLE001
                errs.append({"venue": venue, "symbol": s, "what": "order_book",
                             "error": f"{type(e).__name__}: {str(e)[:150]}"})
        return out, errs

    def fetch_books(self, symbols=CRYPTO_SYMBOLS, depth=20):
        books, errs = {}, []
        with ThreadPoolExecutor(max_workers=len(self.ex) or 1) as pool:
            for b, e in pool.map(lambda v: self._fetch_venue_books(v, symbols, depth), self.ex):
                books.update(b)
                errs.extend(e)
        return books, errs

    def fetch_trades(self, markets=MM_MARKETS):
        out, errs = {}, []
        for venue, s in markets:
            if venue not in self.ex or not self.listed(venue, s):
                errs.append({"venue": venue, "symbol": s, "what": "trades", "error": "NO_DISPONIBLE"})
                continue
            k = Snapshot.k(venue, s)
            try:
                tr = self.ex[venue].fetch_trades(s, since=self.last_trade_ms.get(k), limit=500)
                out[k] = [{"ts": t["timestamp"], "price": float(t["price"]),
                           "amount": float(t["amount"]), "side": t.get("side")} for t in tr]
                if tr:
                    self.last_trade_ms[k] = max(t["timestamp"] for t in tr) + 1
            except Exception as e:  # noqa: BLE001
                errs.append({"venue": venue, "symbol": s, "what": "trades",
                             "error": f"{type(e).__name__}: {str(e)[:150]}"})
        return out, errs


class PolymarketSource:
    """Gamma (eventos) + CLOB (libros). Público y sin claves."""

    def __init__(self, session=None, max_events=150, max_books=200):
        self.s = session or requests.Session()
        self.max_events, self.max_books = max_events, max_books

    def fetch(self):
        errs = []
        try:
            r = self.s.get(f"{GAMMA}/events", params={
                "closed": "false", "active": "true", "limit": self.max_events,
                "order": "volume24hr", "ascending": "false"}, timeout=20)
            r.raise_for_status()
            events = r.json()
        except Exception as e:  # noqa: BLE001
            return {"events": [], "books": {}}, [{"venue": "polymarket", "what": "gamma_events",
                                                  "error": f"{type(e).__name__}: {str(e)[:150]}"}]
        slim = []
        for e in events:
            if not e.get("negRisk"):
                continue
            ms = []
            for m in e.get("markets") or []:
                try:
                    toks = json.loads(m.get("clobTokenIds") or "[]")
                except (TypeError, ValueError):
                    toks = []
                ms.append({k: m.get(k) for k in (
                    "id", "question", "groupItemTitle", "active", "closed", "enableOrderBook",
                    "outcomes",
                    "bestBid", "bestAsk", "orderMinSize", "orderPriceMinTickSize",
                    "feesEnabled", "feeSchedule", "negRisk", "volume24hr")} | {"tokens": toks})
            slim.append({"id": e.get("id"), "slug": e.get("slug"), "title": e.get("title"),
                         "negRisk": True, "markets": ms})
        return {"events": slim, "books": {}}, errs

    def _one_book(self, t):
        try:
            r = self.s.get(f"{CLOB}/book", params={"token_id": t}, timeout=15)
            if r.status_code == 404:
                return t, None, {"venue": "polymarket", "what": "book", "token": t,
                                 "error": "HTTP 404 (sin libro)"}
            r.raise_for_status()
            b = r.json()
            return t, {"bids": sorted([[float(x["price"]), float(x["size"])] for x in b.get("bids", [])], reverse=True),
                       "asks": sorted([[float(x["price"]), float(x["size"])] for x in b.get("asks", [])]),
                       "fetched_at": now_iso()}, None
        except Exception as e:  # noqa: BLE001
            return t, None, {"venue": "polymarket", "what": "book", "token": t,
                             "error": f"{type(e).__name__}: {str(e)[:120]}"}

    def fetch_books(self, token_ids, workers=12):
        books, errs = {}, []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for t, b, e in pool.map(self._one_book, list(dict.fromkeys(token_ids))[:self.max_books]):
                if b is not None:
                    books[t] = b
                if e:
                    errs.append(e)
        return books, errs


FUTURES_VENUES = {
    # venue: (opciones ccxt, quote del spot y de los futuros lineales)
    "binance": ({"options": {"defaultType": "future"}}, "USDT"),
    "bybit": ({}, "USDT"),
    "deribit": ({}, "USDC"),
}
FUTURES_ASSETS = ("BTC", "ETH")
# ¿El libro de futuros LINEALES viene en contratos? Verificado contra la API
# cruda: Deribit lineal ya viene en BTC aunque contractSize=0.0001 (multiplicar
# achicaba la profundidad 10.000x); OKX sí cotiza en contratos.
BOOK_IN_CONTRACTS = {"okx": True, "binance": False, "bybit": False, "deribit": False}
MAX_EXPIRIES = 4


class FuturesSource:
    """Futuros LINEALES con vencimiento + el spot del mismo exchange.

    Cantidades del libro SIEMPRE en unidades del activo (se multiplica por
    contractSize: Deribit/OKX cotizan en contratos)."""

    def __init__(self, venues=FUTURES_VENUES, exchanges=None, now_ms=None):
        self.venues, self.ex, self.meta, self.init_errors = venues, {}, {}, []
        self.now_ms = now_ms
        if exchanges is not None:
            self.ex = exchanges
        else:
            import ccxt
            for v, (opts, _) in venues.items():
                try:
                    e = getattr(ccxt, v)({"enableRateLimit": True, "timeout": 20000, **opts})
                    e.load_markets()
                    self.ex[v] = e
                except Exception as err:  # noqa: BLE001
                    self.init_errors.append({"venue": v, "what": "futures_markets",
                                             "error": f"{type(err).__name__}: {str(err)[:150]}"})
        for e in self.ex.values():
            assert not getattr(e, "apiKey", None), "no se admiten claves"

    def _select(self):
        import time as _t
        now = self.now_ms or int(_t.time() * 1000)
        meta = {}
        for v, e in self.ex.items():
            quote = self.venues.get(v, ({}, "USDT"))[1]
            for asset in FUTURES_ASSETS:
                spot = f"{asset}/{quote}"
                if spot not in e.markets:
                    continue
                futs = sorted((m for m in e.markets.values()
                               if m.get("future") and m.get("linear") and m.get("base") == asset
                               and m.get("settle") == quote and m.get("expiry")
                               and m["expiry"] > now + 86_400_000 and m.get("active", True)),
                              key=lambda m: m["expiry"])[:MAX_EXPIRIES]
                for m in futs:
                    lim = m.get("limits") or {}
                    meta[Snapshot.k(v, m["symbol"])] = {
                        "venue": v, "asset": asset, "symbol": m["symbol"], "spot": spot,
                        "expiry": m["expiry"], "expiry_iso": m.get("expiryDatetime"),
                        "contract_size": float(m.get("contractSize") or 1.0),
                        "min_amount": (lim.get("amount") or {}).get("min"),
                        "min_cost": (lim.get("cost") or {}).get("min"),
                        "taker_ref": m.get("taker"),
                        "spot_min_amount": ((e.markets[spot].get("limits") or {}).get("amount") or {}).get("min"),
                        "spot_taker_ref": e.markets[spot].get("taker")}
        return meta

    def fetch(self, meta_only=False, refresh_meta=True, depth=20):
        """-> (libros {venue|símbolo}, meta, errores). Incluye el spot de cada venue."""
        errs = list(self.init_errors)
        if refresh_meta or not self.meta:
            try:
                self.meta = self._select()
            except Exception as e:  # noqa: BLE001
                errs.append({"venue": "futures", "what": "select", "error": str(e)[:150]})
        books = {}
        wanted = {(m["venue"], m["symbol"],
                   m["contract_size"] if BOOK_IN_CONTRACTS.get(m["venue"], False) else 1.0)
                  for m in self.meta.values()}
        wanted |= {(m["venue"], m["spot"], 1.0) for m in self.meta.values()}
        for v, sym, csize in sorted(wanted):
            try:
                ob = self.ex[v].fetch_order_book(sym, depth)
                books[Snapshot.k(v, sym)] = {
                    "bids": [[float(p), float(q) * csize] for p, q, *_ in ob["bids"][:depth]],
                    "asks": [[float(p), float(q) * csize] for p, q, *_ in ob["asks"][:depth]],
                    "fetched_at": now_iso()}
            except Exception as e:  # noqa: BLE001
                errs.append({"venue": v, "symbol": sym, "what": "futures_book",
                             "error": f"{type(e).__name__}: {str(e)[:120]}"})
        return books, self.meta, errs


SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
JUP_QUOTE = "https://lite-api.jup.ag/swap/v1/quote"
SOLANA_RPC = "https://api.mainnet-beta.solana.com"
DEX_SIZES_USD = (10.0, 25.0, 45.0)


class JupiterSource:
    """Cotizaciones de Jupiter (agregador DEX de Solana), públicas y POR TAMAÑO.

    Una cotización no es una ejecución: el swap puede salir peor (hasta
    otherAmountThreshold, que fija el slippage tolerado) o fallar on-chain.
    """

    def __init__(self, session=None, slippage_bps=50):
        self.s = session or requests.Session()
        self.slippage_bps = slippage_bps

    def quote(self, input_mint, output_mint, amount_raw):
        r = self.s.get(JUP_QUOTE, params={"inputMint": input_mint, "outputMint": output_mint,
                                          "amount": str(int(amount_raw)),
                                          "slippageBps": self.slippage_bps}, timeout=15)
        r.raise_for_status()
        d = r.json()
        return {"in": int(d["inAmount"]), "out": int(d["outAmount"]),
                "min_out": int(d["otherAmountThreshold"]),
                "price_impact_pct": float(d.get("priceImpactPct") or 0),
                "route": [x.get("swapInfo", {}).get("label") for x in d.get("routePlan", [])],
                "slot": d.get("contextSlot"), "fetched_at": now_iso()}

    def priority_fee(self):
        """Mediana de fees de prioridad recientes (micro-lamports por CU)."""
        r = self.s.post(SOLANA_RPC, json={"jsonrpc": "2.0", "id": 1,
                                          "method": "getRecentPrioritizationFees", "params": []},
                        timeout=15)
        fees = sorted(x["prioritizationFee"] for x in r.json().get("result", []))
        return {"median_micro_lamports_per_cu": fees[len(fees) // 2] if fees else None,
                "p90": fees[int(len(fees) * 0.9)] if fees else None, "n": len(fees),
                "fetched_at": now_iso()}

    def quotes_for(self, sol_usd):
        """SOL->USDC y USDC->SOL para cada tamaño en USD. Errores se registran."""
        out, errs = {}, []
        for usd in DEX_SIZES_USD:
            for direction, (i, o, amt) in {
                "SOL->USDC": (SOL_MINT, USDC_MINT, usd / sol_usd * 1e9),
                "USDC->SOL": (USDC_MINT, SOL_MINT, usd * 1e6)}.items():
                k = f"{direction}|{usd:g}"
                try:
                    out[k] = self.quote(i, o, amt)
                except Exception as e:  # noqa: BLE001
                    errs.append({"venue": "jupiter", "what": k,
                                 "error": f"{type(e).__name__}: {str(e)[:120]}"})
        return out, errs


assert PAPER_ONLY
