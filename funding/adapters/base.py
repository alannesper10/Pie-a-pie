"""Adaptador de SOLO LECTURA sobre ccxt para datos públicos.

No se configuran claves de API. Cualquier intento de operar lanza
PaperOnlyError: la interfaz de trading existe solo como lugar reservado para
una etapa futura y no está implementada.
"""

import time
from typing import Dict, List, Optional, Tuple

from ..config import PAPER_ONLY
from ..funding import infer_interval_hours

HOUR_MS = 3_600_000


class PaperOnlyError(RuntimeError):
    pass


class ReadOnlyAdapter:
    name = "base"
    ccxt_id = None
    funding_page_limit = 100
    ohlcv_page_limit = 200
    perp_type = "swap"
    ws_depth_public = "requested"   # profundidad WS sin autenticación

    def ws_depth(self, requested):
        """Profundidad a pedir por WebSocket sin necesitar login."""
        return requested if self.ws_depth_public == "requested" else self.ws_depth_public

    def __init__(self, exchange=None):
        if exchange is None:
            import ccxt  # import tardío: los tests y Actions no necesitan ccxt
            exchange = getattr(ccxt, self.ccxt_id)({"enableRateLimit": True,
                                                    "timeout": 15000})
        # Nunca se cargan claves: apiKey/secret quedan vacíos.
        assert not getattr(exchange, "apiKey", None), "no se admiten claves"
        self.ex = exchange
        self._markets_loaded = False

    # -- símbolos ----------------------------------------------------------
    def spot_symbol(self, asset, quote="USDT"):
        return f"{asset}/{quote}"

    def perp_symbol(self, asset, quote="USDT"):
        return f"{asset}/{quote}:{quote}"

    # -- metadata (REST) ---------------------------------------------------
    def load_markets(self):
        if not self._markets_loaded:
            self.ex.load_markets()
            self._markets_loaded = True

    def market_info(self, asset) -> Dict[str, dict]:
        """Tamaño mínimo, tick, tamaño de contrato y fee de referencia (ccxt)."""
        self.load_markets()
        out = {}
        for kind, sym in (("spot", self.spot_symbol(asset)),
                          ("perp", self.perp_symbol(asset))):
            m = self.ex.market(sym)
            lim = m.get("limits") or {}
            out[kind] = {
                "symbol": sym,
                "min_amount": (lim.get("amount") or {}).get("min"),
                "min_cost": (lim.get("cost") or {}).get("min"),
                "amount_precision": (m.get("precision") or {}).get("amount"),
                "tick_size": (m.get("precision") or {}).get("price"),
                "contract_size": m.get("contractSize") or 1.0,
                "ccxt_taker_fee": m.get("taker"),
                "ccxt_maker_fee": m.get("maker"),
                "funding_interval_h_meta": self.interval_from_market(m),
            }
        return out

    def interval_from_market(self, market) -> Optional[float]:
        return None

    # -- historial (REST, paginado) ----------------------------------------
    def fetch_funding_history(self, asset, since_ms, until_ms=None) -> List[Tuple[int, float]]:
        sym, rows, cursor = self.perp_symbol(asset), {}, since_ms
        until_ms = until_ms or int(time.time() * 1000)
        for _ in range(500):
            page = self.ex.fetch_funding_rate_history(
                sym, since=cursor, limit=self.funding_page_limit)
            fresh = [(int(r["timestamp"]), float(r["fundingRate"])) for r in page
                     if r.get("timestamp") is not None and int(r["timestamp"]) not in rows]
            if not fresh:
                break
            rows.update(fresh)
            last = max(t for t, _ in fresh)
            if last >= until_ms - HOUR_MS or last + 1 <= cursor:
                break
            cursor = last + 1
        return sorted((t, r) for t, r in rows.items() if since_ms <= t <= until_ms)

    def fetch_closes(self, asset, market, since_ms, timeframe="1h",
                     until_ms=None) -> List[Tuple[int, float]]:
        """market: 'spot' | 'perp' | 'mark'. Cierres horarios paginados."""
        sym = self.spot_symbol(asset) if market == "spot" else self.perp_symbol(asset)
        fn = self.ex.fetch_mark_ohlcv if market == "mark" else self.ex.fetch_ohlcv
        rows, cursor = {}, since_ms
        until_ms = until_ms or int(time.time() * 1000)
        for _ in range(500):
            page = fn(sym, timeframe, since=cursor, limit=self.ohlcv_page_limit)
            fresh = [(int(c[0]), float(c[4])) for c in page if int(c[0]) not in rows]
            if not fresh:
                break
            rows.update(fresh)
            last = max(t for t, _ in fresh)
            if last >= until_ms - HOUR_MS or last + 1 <= cursor:
                break
            cursor = last + 1
        return sorted((t, c) for t, c in rows.items() if since_ms <= t <= until_ms)

    # -- vivo (REST; WebSocket en market_data.WsSource) --------------------
    def fetch_funding_now(self, asset) -> dict:
        r = self.ex.fetch_funding_rate(self.perp_symbol(asset))
        interval = r.get("interval")
        hours = None
        if isinstance(interval, str) and interval.endswith("h"):
            hours = float(interval[:-1])
        return {"rate": r.get("fundingRate"), "next_ts": r.get("fundingTimestamp")
                or r.get("nextFundingTimestamp"), "interval_h": hours,
                "mark": r.get("markPrice"), "index": r.get("indexPrice"),
                "timestamp": r.get("timestamp")}

    def fetch_books(self, asset, limit=20) -> dict:
        """Libros con cantidades SIEMPRE en unidades del activo.

        En OKX el perp viene en contratos (ctVal 0.01 BTC): sin convertir, la
        profundidad quedaría 100x inflada.
        """
        self.load_markets()
        csize = float(self.ex.market(self.perp_symbol(asset)).get("contractSize") or 1.0)
        s = self.ex.fetch_order_book(self.spot_symbol(asset), limit=limit)
        p = self.ex.fetch_order_book(self.perp_symbol(asset), limit=limit)
        conv = lambda lv: [[float(px), float(q) * csize] for px, q, *_ in lv]  # noqa: E731
        return {"spot_bids": [[float(a), float(b)] for a, b, *_ in s["bids"]],
                "spot_asks": [[float(a), float(b)] for a, b, *_ in s["asks"]],
                "perp_bids": conv(p["bids"]), "perp_asks": conv(p["asks"]),
                "perp_contract_size": csize,
                "spot_ts": s.get("timestamp"), "perp_ts": p.get("timestamp")}

    def min_qty(self, asset):
        """Cantidad mínima operable (en unidades del activo) para ambas patas."""
        mi = self.market_info(asset)
        spot_q = mi["spot"]["min_amount"] or 0.0
        perp_q = (mi["perp"]["min_amount"] or 0.0) * (mi["perp"]["contract_size"] or 1.0)
        return {"spot_min_qty": spot_q, "spot_min_cost": mi["spot"]["min_cost"] or 0.0,
                "perp_min_qty": perp_q, "perp_min_cost": mi["perp"]["min_cost"] or 0.0}

    def fetch_trading_fees(self):
        """Requiere autenticación en los 3 exchanges: no se usa (UNVERIFIED)."""
        raise PaperOnlyError("las tarifas por cuenta requieren claves; no se usan")

    # -- verificación de endpoints -----------------------------------------
    def probe(self, asset="BTC") -> Dict[str, str]:
        """Prueba cada endpoint público y devuelve OK / ERROR por endpoint."""
        now = int(time.time() * 1000)
        checks = {
            "load_markets": lambda: self.market_info(asset),
            "funding_now": lambda: self.fetch_funding_now(asset),
            "funding_history": lambda: self.fetch_funding_history(asset, now - 3 * 86_400_000),
            "spot_ohlcv": lambda: self.fetch_closes(asset, "spot", now - 6 * HOUR_MS),
            "perp_ohlcv": lambda: self.fetch_closes(asset, "perp", now - 6 * HOUR_MS),
            "mark_ohlcv": lambda: self.fetch_closes(asset, "mark", now - 6 * HOUR_MS),
            "order_books": lambda: self.fetch_books(asset, 5),
            "trading_fees": self.fetch_trading_fees,
        }
        out = {}
        for name, fn in checks.items():
            try:
                res = fn()
                empty = res is None or (hasattr(res, "__len__") and len(res) == 0)
                out[name] = "EMPTY" if empty else "OK"
            except PaperOnlyError as e:
                out[name] = f"AUTH_REQUIRED ({e})"
            except Exception as e:  # noqa: BLE001
                out[name] = f"ERROR {type(e).__name__}: {str(e)[:120]}"
        return out

    # -- trading: deshabilitado --------------------------------------------
    def create_order(self, *args, **kwargs):
        raise PaperOnlyError("paper_only=True: no se envían órdenes reales")

    def withdraw(self, *args, **kwargs):
        raise PaperOnlyError("paper_only=True: no se hacen retiros")


assert PAPER_ONLY, "funding/basis es solo paper trading"
__all__ = ["ReadOnlyAdapter", "PaperOnlyError", "infer_interval_hours"]
