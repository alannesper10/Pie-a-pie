# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 200 (200) | 184 (184) | 184 (184) | 45 |
| Oportunidades | 34068 | 27541 | 27162 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 34068 | 2805977 | 181307302 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.136 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04465 | 0.02217 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.3 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=34068
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1752953, LOW_VOLUME=746873, PRELIM_GROSS_TOO_LOW=154808, OVER_CANDIDATE_CAP=95441, NO_POSITIVE_MARGINAL_EDGE=27589
- strike_inconsistency: NO_QUOTE=133582012, LOW_VOLUME=38656167, PRELIM_GROSS_TOO_LOW=6144173, LEG_NOT_TRADABLE=2774959, OVER_CANDIDATE_CAP=61803
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
