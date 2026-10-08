# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 68 (68) | 52 (52) | 52 (52) | 45 |
| Oportunidades | 7726 | 7784 | 7705 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7726 | 734899 | 50148986 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.288 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05421 | 0.04626 | 0.02232 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 113.6 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7726
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=448513, LOW_VOLUME=207055, PRELIM_GROSS_TOO_LOW=41038, OVER_CANDIDATE_CAP=23140, NO_POSITIVE_MARGINAL_EDGE=7797
- strike_inconsistency: NO_QUOTE=37743161, LOW_VOLUME=9938091, PRELIM_GROSS_TOO_LOW=1566464, LEG_NOT_TRADABLE=860832, GROUPING_MISMATCH=17076
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
