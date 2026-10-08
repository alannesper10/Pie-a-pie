# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 79 (79) | 63 (63) | 63 (63) | 45 |
| Oportunidades | 9299 | 9434 | 9340 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9299 | 901406 | 59882990 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.237 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05422 | 0.0458 | 0.02211 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 117.7 | 149.7 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9299
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=552779, LOW_VOLUME=252107, PRELIM_GROSS_TOO_LOW=49624, OVER_CANDIDATE_CAP=28574, NO_POSITIVE_MARGINAL_EDGE=9447
- strike_inconsistency: NO_QUOTE=44801416, LOW_VOLUME=12183981, PRELIM_GROSS_TOO_LOW=1915570, LEG_NOT_TRADABLE=932142, GROUPING_MISMATCH=20728
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
