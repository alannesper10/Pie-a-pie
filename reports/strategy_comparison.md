# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 94 (94) | 78 (78) | 78 (78) | 45 |
| Oportunidades | 11582 | 11680 | 11529 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 11582 | 1132575 | 75614265 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.189 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05406 | 0.04538 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.2 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=11582
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=696477, LOW_VOLUME=315175, PRELIM_GROSS_TOO_LOW=61473, OVER_CANDIDATE_CAP=36149, NO_POSITIVE_MARGINAL_EDGE=11696
- strike_inconsistency: NO_QUOTE=56749813, LOW_VOLUME=15388078, PRELIM_GROSS_TOO_LOW=2378732, LEG_NOT_TRADABLE=1034181, OVER_CANDIDATE_CAP=25884
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
