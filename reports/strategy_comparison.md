# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 598 (598) | 582 (582) | 582 (582) | 45 |
| Oportunidades | 97569 | 87099 | 85717 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 97567 | 8482534 | 576315734 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.992 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0554 | 0.04305 | 0.02124 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 163.2 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=97498, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5261210, LOW_VOLUME=2284341, PRELIM_GROSS_TOO_LOW=477473, OVER_CANDIDATE_CAP=288187, NO_POSITIVE_MARGINAL_EDGE=87264
- strike_inconsistency: NO_QUOTE=424729716, LOW_VOLUME=125227935, PRELIM_GROSS_TOO_LOW=18671144, LEG_NOT_TRADABLE=7193546, OVER_CANDIDATE_CAP=215132
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
