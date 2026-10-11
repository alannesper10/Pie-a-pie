# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 261 (261) | 245 (245) | 245 (245) | 45 |
| Oportunidades | 46334 | 36666 | 35972 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 46334 | 3678735 | 242604370 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.102 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05533 | 0.04413 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.5 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=46334
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2304993, LOW_VOLUME=969088, PRELIM_GROSS_TOO_LOW=206122, OVER_CANDIDATE_CAP=122925, NO_POSITIVE_MARGINAL_EDGE=36734
- strike_inconsistency: NO_QUOTE=179893323, LOW_VOLUME=51179211, PRELIM_GROSS_TOO_LOW=8036816, LEG_NOT_TRADABLE=3297927, GROUPING_MISMATCH=80249
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
