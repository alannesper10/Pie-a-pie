# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 311 (311) | 295 (295) | 295 (295) | 45 |
| Oportunidades | 53441 | 44151 | 43223 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 53441 | 4316671 | 292091966 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.07 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04373 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.8 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=53441
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2706393, LOW_VOLUME=1133440, PRELIM_GROSS_TOO_LOW=242953, OVER_CANDIDATE_CAP=142442, NO_POSITIVE_MARGINAL_EDGE=44226
- strike_inconsistency: NO_QUOTE=218818500, LOW_VOLUME=60156765, PRELIM_GROSS_TOO_LOW=9204980, LEG_NOT_TRADABLE=3678141, GROUPING_MISMATCH=96108
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
