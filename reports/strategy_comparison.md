# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 33 (33) | 17 (17) | 17 (17) | 45 |
| Oportunidades | 4007 | 2545 | 2514 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4007 | 237932 | 18438411 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.575 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05461 | 0.04936 | 0.02173 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 121.4 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4007
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=144807, LOW_VOLUME=67146, PRELIM_GROSS_TOO_LOW=12608, OVER_CANDIDATE_CAP=8139, NO_POSITIVE_MARGINAL_EDGE=2549
- strike_inconsistency: NO_QUOTE=14347668, LOW_VOLUME=3453601, PRELIM_GROSS_TOO_LOW=517590, LEG_NOT_TRADABLE=104941, OVER_CANDIDATE_CAP=6382
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
