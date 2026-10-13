# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 372 (372) | 356 (356) | 356 (356) | 45 |
| Oportunidades | 61372 | 53286 | 52310 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61370 | 5112200 | 349577796 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.044 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05608 | 0.0435 | 0.0216 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61317, SUSPICIOUS_EDGE_CHECK_RULES=53
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3190255, LOW_VOLUME=1354896, PRELIM_GROSS_TOO_LOW=287984, OVER_CANDIDATE_CAP=170397, NO_POSITIVE_MARGINAL_EDGE=53373
- strike_inconsistency: NO_QUOTE=263427530, LOW_VOLUME=70746979, PRELIM_GROSS_TOO_LOW=10685803, LEG_NOT_TRADABLE=4439619, GROUPING_MISMATCH=116127
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
