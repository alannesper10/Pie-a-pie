from .base import ReadOnlyAdapter


class BinanceAdapter(ReadOnlyAdapter):
    """Binance spot + USDⓈ-M perpetuos (datos públicos)."""
    name = "binance"
    ccxt_id = "binance"
    funding_page_limit = 1000
    ohlcv_page_limit = 1000

    def interval_from_market(self, market):
        # Binance expone el intervalo solo para símbolos ajustados
        # (fapi/v1/fundingInfo); para el resto se infiere del historial.
        return None
