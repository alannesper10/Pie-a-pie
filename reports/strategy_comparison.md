# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 143 (143) | 127 (127) | 127 (127) | 45 |
| Oportunidades | 21014 | 19009 | 18764 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 21014 | 1898283 | 121904801 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.179 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05448 | 0.0453 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 147 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=21014
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1178243, LOW_VOLUME=516703, PRELIM_GROSS_TOO_LOW=103242, OVER_CANDIDATE_CAP=62572, NO_POSITIVE_MARGINAL_EDGE=19041
- strike_inconsistency: NO_QUOTE=90568506, LOW_VOLUME=25392890, PRELIM_GROSS_TOO_LOW=3967023, LEG_NOT_TRADABLE=1873919, GROUPING_MISMATCH=41646
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
