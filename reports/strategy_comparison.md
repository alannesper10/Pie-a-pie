# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 310 (310) | 294 (294) | 294 (294) | 45 |
| Oportunidades | 53299 | 44001 | 43073 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 53299 | 4304279 | 291098475 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.07 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04374 | 0.02185 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.9 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=53299
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2698689, LOW_VOLUME=1130171, PRELIM_GROSS_TOO_LOW=242243, OVER_CANDIDATE_CAP=142022, NO_POSITIVE_MARGINAL_EDGE=44076
- strike_inconsistency: NO_QUOTE=218021099, LOW_VOLUME=59989147, PRELIM_GROSS_TOO_LOW=9184107, LEG_NOT_TRADABLE=3671196, GROUPING_MISMATCH=95799
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
