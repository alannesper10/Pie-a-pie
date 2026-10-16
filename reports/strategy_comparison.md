# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 512 (512) | 496 (496) | 496 (496) | 45 |
| Oportunidades | 81050 | 74236 | 73045 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 81048 | 7158529 | 485761313 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.001 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05573 | 0.0431 | 0.02131 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 158.3 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=80979, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4431874, LOW_VOLUME=1932361, PRELIM_GROSS_TOO_LOW=404963, OVER_CANDIDATE_CAP=242308, NO_POSITIVE_MARGINAL_EDGE=74367
- strike_inconsistency: NO_QUOTE=361648649, LOW_VOLUME=102219380, PRELIM_GROSS_TOO_LOW=15119905, LEG_NOT_TRADABLE=6374834, OVER_CANDIDATE_CAP=161919
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
