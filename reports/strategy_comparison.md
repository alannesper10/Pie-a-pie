# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 941 (941) | 925 (924) | 925 (924) | 45 |
| Oportunidades | 147146 | 138288 | 136133 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 147144 | 14018828 | 1042466158 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.925 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05493 | 0.04215 | 0.02103 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.4 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=147075, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8382613, LOW_VOLUME=4114650, PRELIM_GROSS_TOO_LOW=779324, OVER_CANDIDATE_CAP=464470, NO_POSITIVE_MARGINAL_EDGE=138547
- strike_inconsistency: NO_QUOTE=781208202, LOW_VOLUME=215043835, PRELIM_GROSS_TOO_LOW=30991713, LEG_NOT_TRADABLE=14369387, OVER_CANDIDATE_CAP=410142
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
