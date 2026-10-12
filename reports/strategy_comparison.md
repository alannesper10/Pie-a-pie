# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 293 (293) | 277 (277) | 277 (277) | 45 |
| Oportunidades | 51031 | 41456 | 40554 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 51031 | 4091980 | 274218298 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.078 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05552 | 0.04383 | 0.02192 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 174.2 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=51031
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2567217, LOW_VOLUME=1073473, PRELIM_GROSS_TOO_LOW=230590, OVER_CANDIDATE_CAP=134860, NO_POSITIVE_MARGINAL_EDGE=41527
- strike_inconsistency: NO_QUOTE=204516523, LOW_VOLUME=57082875, PRELIM_GROSS_TOO_LOW=8846427, LEG_NOT_TRADABLE=3550739, GROUPING_MISMATCH=90546
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
