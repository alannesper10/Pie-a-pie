# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 555 (555) | 539 (539) | 539 (539) | 45 |
| Oportunidades | 90163 | 80667 | 79451 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 90161 | 7854990 | 531982202 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.994 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05552 | 0.04307 | 0.02123 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.5 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=90092, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4870521, LOW_VOLUME=2114536, PRELIM_GROSS_TOO_LOW=442963, OVER_CANDIDATE_CAP=268344, NO_POSITIVE_MARGINAL_EDGE=80814
- strike_inconsistency: NO_QUOTE=392665213, LOW_VOLUME=114964786, PRELIM_GROSS_TOO_LOW=17140360, LEG_NOT_TRADABLE=6764054, OVER_CANDIDATE_CAP=190268
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
