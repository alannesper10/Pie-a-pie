from dataclasses import dataclass

@dataclass(frozen=True)
class BotConfig:
    starting_capital_usd: float = 100.0
    external_contributions_usd: float = 0.0
    min_net_edge: float = 0.005
    max_capital_per_trade: float = 0.10
    estimated_slippage: float = 0.001  # USD por contrato y por pata
    estimated_fees: float = 0.0
    paper_only: bool = True

    # Comisión taker de Kalshi: ceil_centavo(coef * C * P * (1 - P)) por pata.
    taker_fee_coefficient: float = 0.07


@dataclass(frozen=True)
class ScannerConfig:
    # Rate limit tier Basic: 200 tokens/s de lectura, ~10 tokens por GET.
    read_tokens_per_second: float = 200.0
    tokens_per_read: float = 10.0
    max_workers: int = 8
    request_timeout_s: float = 10.0
    max_retries: int = 4

    # Paginación de GET /events (máx 200 por página).
    events_page_size: int = 200

    # Prefiltro previo a pedir orderbooks.
    min_event_volume_24h: float = 100.0   # contratos, sumando todas las patas
    min_leg_ask_size: float = 1.0         # cada pata necesita ask con tamaño
    max_prelim_sum: float = 1.05          # suma de YES ask (top of book) a considerar
    min_sane_ask_sum: float = 0.90        # por debajo: sospechoso, revisar reglas

    # Límites por corrida.
    max_events_per_run: int = 50
    event_timeout_s: float = 15.0

    # Caché de eventos filtrados (estructura, no precios).
    cache_refresh_min: float = 30.0
