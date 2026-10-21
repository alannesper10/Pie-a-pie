# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 694 (694) | 678 (678) | 678 (678) | 45 |
| Oportunidades | 108845 | 101471 | 99741 | 0 |
| Net-positive | 2 | 0 | 12 | 0 |
| Ejecutables | 2 | 0 | 11 | 0 |
| Descartadas | 108843 | 9773063 | 670872892 | 2412 |
| Duración media (min) | 0 | n/d | 22.72 | n/d |
| Capital por paquete (media) | 1.014 | 1.985 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05523 | 0.04289 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.8 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=108774, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6044883, LOW_VOLUME=2647743, PRELIM_GROSS_TOO_LOW=550121, OVER_CANDIDATE_CAP=332175, NO_POSITIVE_MARGINAL_EDGE=101659
- strike_inconsistency: NO_QUOTE=493748176, LOW_VOLUME=146375535, PRELIM_GROSS_TOO_LOW=21610956, LEG_NOT_TRADABLE=8560000, OVER_CANDIDATE_CAP=254987
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
