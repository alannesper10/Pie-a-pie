# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 371 (371) | 355 (355) | 355 (355) | 45 |
| Oportunidades | 61249 | 53136 | 52160 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61247 | 5098846 | 348552108 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.044 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05608 | 0.04351 | 0.0216 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.1 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61195, SUSPICIOUS_EDGE_CHECK_RULES=52
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3182251, LOW_VOLUME=1351090, PRELIM_GROSS_TOO_LOW=287213, OVER_CANDIDATE_CAP=169882, NO_POSITIVE_MARGINAL_EDGE=53223
- strike_inconsistency: NO_QUOTE=262611542, LOW_VOLUME=70569576, PRELIM_GROSS_TOO_LOW=10661187, LEG_NOT_TRADABLE=4432683, GROUPING_MISMATCH=115796
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
