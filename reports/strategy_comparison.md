# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 255 (255) | 239 (239) | 239 (239) | 45 |
| Oportunidades | 45068 | 35766 | 35084 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 45068 | 3596799 | 236569674 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.109 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05527 | 0.0442 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 176.7 | 149.6 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=45068
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2252799, LOW_VOLUME=948685, PRELIM_GROSS_TOO_LOW=201217, OVER_CANDIDATE_CAP=120357, NO_POSITIVE_MARGINAL_EDGE=35834
- strike_inconsistency: NO_QUOTE=175273760, LOW_VOLUME=49973543, PRELIM_GROSS_TOO_LOW=7871994, LEG_NOT_TRADABLE=3257081, OVER_CANDIDATE_CAP=78655
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
