# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 279 (279) | 263 (263) | 263 (263) | 45 |
| Oportunidades | 49262 | 39363 | 38530 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 49262 | 3916768 | 260579528 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.085 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05546 | 0.04391 | 0.022 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 176.6 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=49262
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2456881, LOW_VOLUME=1028195, PRELIM_GROSS_TOO_LOW=220652, OVER_CANDIDATE_CAP=129780, NO_POSITIVE_MARGINAL_EDGE=39432
- strike_inconsistency: NO_QUOTE=193761115, LOW_VOLUME=54611817, PRELIM_GROSS_TOO_LOW=8558365, LEG_NOT_TRADABLE=3437072, GROUPING_MISMATCH=86093
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
