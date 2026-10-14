# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 404 (404) | 388 (388) | 388 (388) | 45 |
| Oportunidades | 65224 | 58073 | 57053 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 65222 | 5550270 | 379007986 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.03 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05611 | 0.04334 | 0.02151 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.4 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=65153, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3454827, LOW_VOLUME=1479076, PRELIM_GROSS_TOO_LOW=313114, OVER_CANDIDATE_CAP=185982, NO_POSITIVE_MARGINAL_EDGE=58171
- strike_inconsistency: NO_QUOTE=285326203, LOW_VOLUME=76718784, PRELIM_GROSS_TOO_LOW=11551843, LEG_NOT_TRADABLE=5106348, GROUPING_MISMATCH=126524
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
