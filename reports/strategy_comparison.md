# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 863 (863) | 847 (846) | 847 (846) | 45 |
| Oportunidades | 135278 | 126617 | 124622 | 0 |
| Net-positive | 2 | 0 | 44 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 135276 | 12431753 | 844541077 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.951 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05513 | 0.04239 | 0.02108 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.8 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=135207, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7659899, LOW_VOLUME=3385173, PRELIM_GROSS_TOO_LOW=707945, OVER_CANDIDATE_CAP=431727, NO_POSITIVE_MARGINAL_EDGE=126850
- strike_inconsistency: NO_QUOTE=611627094, LOW_VOLUME=192745060, PRELIM_GROSS_TOO_LOW=28203804, LEG_NOT_TRADABLE=11220117, OVER_CANDIDATE_CAP=342016
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
