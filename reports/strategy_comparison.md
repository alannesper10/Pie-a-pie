# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 691 (691) | 675 (675) | 675 (675) | 45 |
| Oportunidades | 108525 | 101022 | 99305 | 0 |
| Net-positive | 2 | 0 | 9 | 0 |
| Ejecutables | 2 | 0 | 8 | 0 |
| Descartadas | 108523 | 9728772 | 667633447 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.985 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05523 | 0.0429 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 23.28 | n/d |
| Oport. por ciclo | 157.1 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=108454, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6018689, LOW_VOLUME=2634422, PRELIM_GROSS_TOO_LOW=547783, OVER_CANDIDATE_CAP=330596, NO_POSITIVE_MARGINAL_EDGE=101209
- strike_inconsistency: NO_QUOTE=491434367, LOW_VOLUME=145611662, PRELIM_GROSS_TOO_LOW=21491987, LEG_NOT_TRADABLE=8522173, OVER_CANDIDATE_CAP=251442
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
