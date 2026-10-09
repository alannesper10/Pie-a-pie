# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 98 (98) | 82 (82) | 82 (82) | 45 |
| Oportunidades | 12269 | 12279 | 12123 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12269 | 1194006 | 79762789 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05408 | 0.04535 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 125.2 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12269
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=734508, LOW_VOLUME=331968, PRELIM_GROSS_TOO_LOW=64693, OVER_CANDIDATE_CAP=38287, NO_POSITIVE_MARGINAL_EDGE=12296
- strike_inconsistency: NO_QUOTE=59917974, LOW_VOLUME=16224039, PRELIM_GROSS_TOO_LOW=2494828, LEG_NOT_TRADABLE=1059468, GROUPING_MISMATCH=27021
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
