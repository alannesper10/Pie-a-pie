# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 539 (539) | 523 (523) | 523 (523) | 45 |
| Oportunidades | 86902 | 78274 | 77062 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 86900 | 7598543 | 514710302 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.998 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05562 | 0.04308 | 0.02126 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.2 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=86831, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4708105, LOW_VOLUME=2048008, PRELIM_GROSS_TOO_LOW=428854, OVER_CANDIDATE_CAP=259174, NO_POSITIVE_MARGINAL_EDGE=78414
- strike_inconsistency: NO_QUOTE=380990954, LOW_VOLUME=110340979, PRELIM_GROSS_TOO_LOW=16332443, LEG_NOT_TRADABLE=6617021, OVER_CANDIDATE_CAP=179356
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
