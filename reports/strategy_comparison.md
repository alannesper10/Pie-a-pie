# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 175 (175) | 159 (159) | 159 (159) | 45 |
| Oportunidades | 28474 | 23801 | 23464 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 28474 | 2412224 | 155084903 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.153 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05489 | 0.04496 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 162.7 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=28474
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1501424, LOW_VOLUME=649273, PRELIM_GROSS_TOO_LOW=131932, OVER_CANDIDATE_CAP=81617, NO_POSITIVE_MARGINAL_EDGE=23841
- strike_inconsistency: NO_QUOTE=114611020, LOW_VOLUME=32983745, PRELIM_GROSS_TOO_LOW=5131741, LEG_NOT_TRADABLE=2229263, OVER_CANDIDATE_CAP=52920
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
