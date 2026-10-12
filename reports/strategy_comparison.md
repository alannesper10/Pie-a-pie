# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 303 (303) | 287 (287) | 287 (287) | 45 |
| Oportunidades | 52305 | 42955 | 42024 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52305 | 4217310 | 284175498 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.073 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05557 | 0.04377 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.6 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52305
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2644792, LOW_VOLUME=1107053, PRELIM_GROSS_TOO_LOW=237402, OVER_CANDIDATE_CAP=138969, NO_POSITIVE_MARGINAL_EDGE=43027
- strike_inconsistency: NO_QUOTE=212476957, LOW_VOLUME=58807202, PRELIM_GROSS_TOO_LOW=9040375, LEG_NOT_TRADABLE=3622581, GROUPING_MISMATCH=93636
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
