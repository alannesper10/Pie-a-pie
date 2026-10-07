from .base import ReadOnlyAdapter


class BybitAdapter(ReadOnlyAdapter):
    """Bybit spot + perpetuos lineales USDT (datos públicos, API v5)."""
    name = "bybit"
    ccxt_id = "bybit"
    funding_page_limit = 200
    ohlcv_page_limit = 1000

    def interval_from_market(self, market):
        # instruments-info trae fundingInterval en minutos para perpetuos.
        minutes = (market.get("info") or {}).get("fundingInterval")
        try:
            return float(minutes) / 60 if minutes else None
        except (TypeError, ValueError):
            return None
