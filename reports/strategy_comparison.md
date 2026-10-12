# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 328 (328) | 312 (312) | 312 (312) | 45 |
| Oportunidades | 55976 | 46697 | 45763 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55976 | 4529068 | 307582376 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.058 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04363 | 0.02177 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.7 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55976
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2838718, LOW_VOLUME=1189293, PRELIM_GROSS_TOO_LOW=255371, OVER_CANDIDATE_CAP=149372, NO_POSITIVE_MARGINAL_EDGE=46776
- strike_inconsistency: NO_QUOTE=231033906, LOW_VOLUME=62905804, PRELIM_GROSS_TOO_LOW=9596103, LEG_NOT_TRADABLE=3801838, GROUPING_MISMATCH=101453
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
