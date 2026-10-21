# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 705 (705) | 689 (689) | 689 (689) | 45 |
| Oportunidades | 110197 | 103120 | 101378 | 0 |
| Net-positive | 2 | 0 | 23 | 0 |
| Ejecutables | 2 | 0 | 22 | 0 |
| Descartadas | 110195 | 9935894 | 682694997 | 2412 |
| Duración media (min) | 0 | n/d | 23.85 | n/d |
| Capital por paquete (media) | 1.014 | 1.983 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04286 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.3 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110126, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6140380, LOW_VOLUME=2696993, PRELIM_GROSS_TOO_LOW=559398, OVER_CANDIDATE_CAP=338121, NO_POSITIVE_MARGINAL_EDGE=103309
- strike_inconsistency: NO_QUOTE=502333087, LOW_VOLUME=149073937, PRELIM_GROSS_TOO_LOW=22002223, LEG_NOT_TRADABLE=8697401, OVER_CANDIDATE_CAP=260005
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
