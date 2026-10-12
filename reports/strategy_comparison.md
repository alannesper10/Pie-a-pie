# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 314 (314) | 298 (298) | 298 (298) | 45 |
| Oportunidades | 53878 | 44601 | 43673 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 53878 | 4353808 | 295072296 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.068 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04371 | 0.02183 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.6 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=53878
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2729505, LOW_VOLUME=1143221, PRELIM_GROSS_TOO_LOW=245146, OVER_CANDIDATE_CAP=143636, NO_POSITIVE_MARGINAL_EDGE=44676
- strike_inconsistency: NO_QUOTE=221209038, LOW_VOLUME=60661205, PRELIM_GROSS_TOO_LOW=9267582, LEG_NOT_TRADABLE=3698961, GROUPING_MISMATCH=97035
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
