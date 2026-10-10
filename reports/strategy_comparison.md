# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 213 (213) | 197 (197) | 197 (197) | 45 |
| Oportunidades | 36552 | 29486 | 28974 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 36552 | 3002471 | 194380180 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.141 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04465 | 0.0221 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.6 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=36552
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1878455, LOW_VOLUME=795853, PRELIM_GROSS_TOO_LOW=166119, OVER_CANDIDATE_CAP=101712, NO_POSITIVE_MARGINAL_EDGE=29538
- strike_inconsistency: NO_QUOTE=143119852, LOW_VOLUME=41452077, PRELIM_GROSS_TOO_LOW=6682928, LEG_NOT_TRADABLE=2961710, OVER_CANDIDATE_CAP=69133
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
