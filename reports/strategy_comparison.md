# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 103 (103) | 87 (87) | 87 (87) | 45 |
| Oportunidades | 13139 | 13029 | 12870 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 13139 | 1270751 | 84975576 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.186 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05409 | 0.0453 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 127.6 | 149.8 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=13139
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=782060, LOW_VOLUME=352822, PRELIM_GROSS_TOO_LOW=68846, OVER_CANDIDATE_CAP=40990, NO_POSITIVE_MARGINAL_EDGE=13046
- strike_inconsistency: NO_QUOTE=63920906, LOW_VOLUME=17250280, PRELIM_GROSS_TOO_LOW=2642171, LEG_NOT_TRADABLE=1092055, GROUPING_MISMATCH=28646
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
