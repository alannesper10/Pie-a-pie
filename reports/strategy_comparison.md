# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 285 (285) | 269 (269) | 269 (269) | 45 |
| Oportunidades | 50036 | 40262 | 39405 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50036 | 3992428 | 266260158 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.081 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05549 | 0.04387 | 0.02196 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 175.6 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50036
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2504798, LOW_VOLUME=1047537, PRELIM_GROSS_TOO_LOW=225041, OVER_CANDIDATE_CAP=131878, NO_POSITIVE_MARGINAL_EDGE=40331
- strike_inconsistency: NO_QUOTE=198176481, LOW_VOLUME=55692649, PRELIM_GROSS_TOO_LOW=8686961, LEG_NOT_TRADABLE=3487935, GROUPING_MISMATCH=88013
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
