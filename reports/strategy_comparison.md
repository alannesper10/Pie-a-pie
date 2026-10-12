# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 309 (309) | 293 (293) | 293 (293) | 45 |
| Oportunidades | 53157 | 43851 | 42923 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 53157 | 4291874 | 290109281 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.071 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04375 | 0.02185 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=53157
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2690990, LOW_VOLUME=1126887, PRELIM_GROSS_TOO_LOW=241540, OVER_CANDIDATE_CAP=141594, NO_POSITIVE_MARGINAL_EDGE=43926
- strike_inconsistency: NO_QUOTE=217226584, LOW_VOLUME=59822750, PRELIM_GROSS_TOO_LOW=9163421, LEG_NOT_TRADABLE=3664251, GROUPING_MISMATCH=95490
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
