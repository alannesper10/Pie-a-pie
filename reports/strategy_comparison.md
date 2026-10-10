# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 150 (150) | 134 (134) | 134 (134) | 45 |
| Oportunidades | 22461 | 20059 | 19785 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 22461 | 2011381 | 129200912 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.172 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05458 | 0.04523 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 149.7 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=22461
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1249729, LOW_VOLUME=545783, PRELIM_GROSS_TOO_LOW=109534, OVER_CANDIDATE_CAP=66598, NO_POSITIVE_MARGINAL_EDGE=20091
- strike_inconsistency: NO_QUOTE=95833735, LOW_VOLUME=27099796, PRELIM_GROSS_TOO_LOW=4239283, LEG_NOT_TRADABLE=1918487, OVER_CANDIDATE_CAP=45322
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
