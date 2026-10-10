# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 165 (165) | 149 (149) | 149 (149) | 45 |
| Oportunidades | 25988 | 22305 | 21973 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 25988 | 2252889 | 144681759 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.156 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05478 | 0.04505 | 0.02194 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 157.5 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=25988
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1401135, LOW_VOLUME=608418, PRELIM_GROSS_TOO_LOW=122893, OVER_CANDIDATE_CAP=75561, NO_POSITIVE_MARGINAL_EDGE=22341
- strike_inconsistency: NO_QUOTE=107108543, LOW_VOLUME=30658513, PRELIM_GROSS_TOO_LOW=4774363, LEG_NOT_TRADABLE=2018756, OVER_CANDIDATE_CAP=50140
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
