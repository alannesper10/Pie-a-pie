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
CRYPTO_SYMBOLS = ("BTC/USDT", "ETH/USDT", "SOL/USDT", "ETH/BTC", "SOL/BTC", "SOL/ETH")
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
            "kalshi", "errors", "latency_ms")}, default=str)

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


assert PAPER_ONLY
