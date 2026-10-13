# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 365 (365) | 349 (349) | 349 (349) | 45 |
| Oportunidades | 60513 | 52237 | 51261 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 60511 | 5018344 | 342401450 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.046 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05603 | 0.04353 | 0.02163 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.8 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60465, SUSPICIOUS_EDGE_CHECK_RULES=46
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3134153, LOW_VOLUME=1328096, PRELIM_GROSS_TOO_LOW=282513, OVER_CANDIDATE_CAP=166728, NO_POSITIVE_MARGINAL_EDGE=52323
- strike_inconsistency: NO_QUOTE=257720124, LOW_VOLUME=69503551, PRELIM_GROSS_TOO_LOW=10514172, LEG_NOT_TRADABLE=4391124, GROUPING_MISMATCH=113810
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
