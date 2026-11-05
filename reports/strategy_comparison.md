# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 892 (892) | 876 (875) | 876 (875) | 45 |
| Oportunidades | 140255 | 130954 | 128843 | 0 |
| Net-positive | 2 | 0 | 48 | 0 |
| Ejecutables | 2 | 0 | 44 | 0 |
| Descartadas | 140253 | 13008696 | 885454196 | 2412 |
| Duración media (min) | 0 | n/d | 19.12 | n/d |
| Capital por paquete (media) | 1.014 | 1.939 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05508 | 0.04222 | 0.02107 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 637.3 | n/d |
| Oport. por ciclo | 157.2 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=140184, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7932861, LOW_VOLUME=3632934, PRELIM_GROSS_TOO_LOW=735043, OVER_CANDIDATE_CAP=448613, NO_POSITIVE_MARGINAL_EDGE=131199
- strike_inconsistency: NO_QUOTE=642736568, LOW_VOLUME=200618237, PRELIM_GROSS_TOO_LOW=29306898, LEG_NOT_TRADABLE=11994367, OVER_CANDIDATE_CAP=380622
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
