from .base import ReadOnlyAdapter


class OkxAdapter(ReadOnlyAdapter):
    """OKX spot + perpetuos SWAP USDT (datos públicos, API v5).

    Ojo: en OKX el perpetuo se opera en contratos (ctVal, ej. 0.01 BTC); el
    tamaño mínimo se expresa en contratos y hay que multiplicar por
    contract_size para obtener la cantidad del activo.
    """
    name = "okx"
    ccxt_id = "okx"
    funding_page_limit = 100
    ohlcv_page_limit = 100
    # Verificado: con profundidad 50 ccxt usa un canal que exige login
    # ("requires authentication for self depth"); el canal completo (400
    # niveles) es público. Se pide entero y se recorta.
    ws_depth_public = None
