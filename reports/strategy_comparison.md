# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 152 (152) | 136 (136) | 136 (136) | 45 |
| Oportunidades | 22895 | 20358 | 20068 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 22895 | 2043882 | 131285785 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.169 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05461 | 0.0452 | 0.02186 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 150.6 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=22895
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1270135, LOW_VOLUME=554224, PRELIM_GROSS_TOO_LOW=111311, OVER_CANDIDATE_CAP=67764, NO_POSITIVE_MARGINAL_EDGE=20391
- strike_inconsistency: NO_QUOTE=97346343, LOW_VOLUME=27581842, PRELIM_GROSS_TOO_LOW=4314675, LEG_NOT_TRADABLE=1931468, OVER_CANDIDATE_CAP=46214
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
