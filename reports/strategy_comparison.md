# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 225 (225) | 209 (209) | 209 (209) | 45 |
| Oportunidades | 38766 | 31277 | 30676 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 38766 | 3178366 | 206614921 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.137 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05498 | 0.04456 | 0.02201 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.3 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=38766
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1989846, LOW_VOLUME=840413, PRELIM_GROSS_TOO_LOW=176547, OVER_CANDIDATE_CAP=106956, NO_POSITIVE_MARGINAL_EDGE=31336
- strike_inconsistency: NO_QUOTE=152337653, LOW_VOLUME=43955507, PRELIM_GROSS_TOO_LOW=7095484, LEG_NOT_TRADABLE=3051606, OVER_CANDIDATE_CAP=74382
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
