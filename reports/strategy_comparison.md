# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 35 (35) | 19 (19) | 19 (19) | 45 |
| Oportunidades | 4235 | 2845 | 2811 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4235 | 266142 | 20203316 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.578 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05456 | 0.04937 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 121 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4235
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=161761, LOW_VOLUME=75323, PRELIM_GROSS_TOO_LOW=14113, OVER_CANDIDATE_CAP=9132, NO_POSITIVE_MARGINAL_EDGE=2849
- strike_inconsistency: NO_QUOTE=15638614, LOW_VOLUME=3856740, PRELIM_GROSS_TOO_LOW=575891, LEG_NOT_TRADABLE=115982, OVER_CANDIDATE_CAP=6906
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
