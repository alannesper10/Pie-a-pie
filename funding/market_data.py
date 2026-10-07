"""Fuentes de libros: REST (por defecto) y WebSocket (ccxt.pro, opcional).

La lógica de decisión no sabe de dónde vienen los libros: recibe un dict con
spot_bids/spot_asks/perp_bids/perp_asks en unidades del activo.
"""

import asyncio
import threading
import time


class RestBooks:
    def __init__(self, adapters):
        self.adapters = adapters

    def get(self, exchange, asset, limit=50):
        return self.adapters[exchange].fetch_books(asset, limit)

    def close(self):
        pass


class WsBooks:
    """Mantiene los últimos libros por WebSocket en un hilo con su event loop.

    Requiere ccxt (ccxt.pro viene incluido). Si un stream falla, `get` cae a
    REST para ese par y el error queda registrado en `errors`.
    """

    def __init__(self, adapters, pairs, limit=50):
        import ccxt.pro as ccxtpro
        self.adapters, self.pairs, self.limit = adapters, pairs, limit
        self.books, self.errors, self.updates = {}, [], {}
        self._stop = False
        self._clients = {name: getattr(ccxtpro, a.ccxt_id)({"enableRateLimit": True})
                         for name, a in adapters.items()}
        self._loop = asyncio.new_event_loop()
        self._tasks, self._ready = [], threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        asyncio.set_event_loop(self._loop)
        for ex, asset in self.pairs:
            a = self.adapters[ex]
            for kind, sym in (("spot", a.spot_symbol(asset)), ("perp", a.perp_symbol(asset))):
                self._tasks.append(self._loop.create_task(self._watch(ex, asset, kind, sym)))
        self._ready.set()
        self._loop.run_forever()
        self._loop.close()

    async def _watch(self, ex, asset, kind, sym):
        client = self._clients[ex]
        csize = 1.0
        while not self._stop:
            try:
                if kind == "perp" and csize == 1.0:
                    await client.load_markets()
                    csize = float(client.market(sym).get("contractSize") or 1.0)
                ob = await client.watch_order_book(
                    sym, self.adapters[ex].ws_depth(self.limit))
                k = 1.0 if kind == "spot" else csize
                self.books[(ex, asset, kind)] = (
                    [[float(p), float(q) * k] for p, q, *_ in ob["bids"][:self.limit]],
                    [[float(p), float(q) * k] for p, q, *_ in ob["asks"][:self.limit]],
                    time.time())
                self.updates[(ex, asset, kind)] = self.updates.get((ex, asset, kind), 0) + 1
            except Exception as e:  # noqa: BLE001
                self.errors.append((ex, sym, f"{type(e).__name__}: {str(e)[:120]}"))
                await asyncio.sleep(5)

    def get(self, exchange, asset, limit=50, max_age_s=10):
        s = self.books.get((exchange, asset, "spot"))
        p = self.books.get((exchange, asset, "perp"))
        now = time.time()
        if not s or not p or now - s[2] > max_age_s or now - p[2] > max_age_s:
            return self.adapters[exchange].fetch_books(asset, limit)   # REST
        return {"spot_bids": s[0], "spot_asks": s[1], "perp_bids": p[0],
                "perp_asks": p[1], "source": "ws"}

    def close(self):
        """Apagado ordenado: cancelar streams, esperarlos, cerrar clientes y
        recién ahí detener el loop (si no, quedan conexiones abiertas)."""
        self._stop = True
        self._ready.wait(10)

        async def _shutdown():
            for t in self._tasks:
                t.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            for c in self._clients.values():
                try:
                    await c.close()
                except Exception:  # noqa: BLE001
                    pass

        try:
            asyncio.run_coroutine_threadsafe(_shutdown(), self._loop).result(20)
        except Exception:  # noqa: BLE001
            pass
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=10)
