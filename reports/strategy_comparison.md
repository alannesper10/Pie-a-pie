# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 78 (78) | 62 (62) | 62 (62) | 45 |
| Oportunidades | 9145 | 9284 | 9192 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9145 | 886177 | 58832631 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.241 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05422 | 0.04583 | 0.02213 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 117.2 | 149.7 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9145
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=543216, LOW_VOLUME=248049, PRELIM_GROSS_TOO_LOW=48821, OVER_CANDIDATE_CAP=28071, NO_POSITIVE_MARGINAL_EDGE=9297
- strike_inconsistency: NO_QUOTE=44003508, LOW_VOLUME=11971978, PRELIM_GROSS_TOO_LOW=1882203, LEG_NOT_TRADABLE=925888, GROUPING_MISMATCH=20396
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
