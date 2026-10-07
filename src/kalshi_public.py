import threading
import time

import requests
from requests.adapters import HTTPAdapter

BASE_URL = "https://external-api.kalshi.com/trade-api/v2"


class TokenBucket:
    """Rate limiter thread-safe: `rate` tokens/s, capacidad de 1 segundo."""

    def __init__(self, rate, capacity=None):
        self.rate = float(rate)
        self.capacity = float(capacity if capacity is not None else rate)
        self.tokens = self.capacity
        self.updated = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, cost):
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(
                    self.capacity, self.tokens + (now - self.updated) * self.rate
                )
                self.updated = now
                if self.tokens >= cost:
                    self.tokens -= cost
                    return
                wait = (cost - self.tokens) / self.rate
            time.sleep(wait)


class KalshiPublicClient:
    """Cliente de lectura de market data. No usa credenciales ni envía órdenes."""

    def __init__(
        self,
        timeout=10,
        tokens_per_second=200.0,
        tokens_per_read=10.0,
        max_retries=4,
        pool_size=16,
    ):
        self.timeout = timeout
        self.tokens_per_read = tokens_per_read
        self.max_retries = max_retries
        self.pool_size = pool_size
        self.bucket = TokenBucket(tokens_per_second)
        self._local = threading.local()

    def _session(self):
        # Una Session por hilo: requests.Session no garantiza ser thread-safe.
        s = getattr(self._local, "session", None)
        if s is None:
            s = requests.Session()
            adapter = HTTPAdapter(
                pool_connections=self.pool_size, pool_maxsize=self.pool_size
            )
            s.mount("https://", adapter)
            self._local.session = s
        return s

    def get(self, path, params=None, timeout=None):
        url = f"{BASE_URL}/{path.lstrip('/')}"
        timeout = self.timeout if timeout is None else timeout
        backoff = 0.5
        for attempt in range(self.max_retries + 1):
            self.bucket.acquire(self.tokens_per_read)
            try:
                r = self._session().get(url, params=params, timeout=timeout)
            except (requests.ConnectionError, requests.Timeout):
                if attempt == self.max_retries:
                    raise
            else:
                # 429 no trae Retry-After: backoff exponencial según la doc.
                if r.status_code != 429 and r.status_code < 500:
                    r.raise_for_status()
                    return r.json()
                if attempt == self.max_retries:
                    r.raise_for_status()
            time.sleep(backoff)
            backoff *= 2

    def get_exchange_announcements(self):
        return self.get("exchange/announcements")

    def iter_events(self, status="open", with_nested_markets=True, limit=200,
                    max_pages=None):
        """Pagina GET /events con cursor. Devuelve eventos de a uno."""
        cursor = None
        pages = 0
        while True:
            params = {
                "status": status,
                "with_nested_markets": str(with_nested_markets).lower(),
                "limit": limit,
            }
            if cursor:
                params["cursor"] = cursor
            data = self.get("events", params=params)
            pages += 1
            yield from data.get("events", [])
            cursor = data.get("cursor")
            if not cursor or (max_pages and pages >= max_pages):
                return

    def get_orderbook(self, ticker, depth=0, timeout=None):
        return self.get(
            f"markets/{ticker}/orderbook", params={"depth": depth}, timeout=timeout
        )
