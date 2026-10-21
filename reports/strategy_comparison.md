# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 696 (696) | 680 (680) | 680 (680) | 45 |
| Oportunidades | 109080 | 101771 | 100036 | 0 |
| Net-positive | 2 | 0 | 14 | 0 |
| Ejecutables | 2 | 0 | 13 | 0 |
| Descartadas | 109078 | 9802857 | 673032510 | 2412 |
| Duración media (min) | 0 | n/d | 24.94 | n/d |
| Capital por paquete (media) | 1.014 | 1.985 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05523 | 0.04288 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.7 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=109009, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6062298, LOW_VOLUME=2656872, PRELIM_GROSS_TOO_LOW=551714, OVER_CANDIDATE_CAP=333255, NO_POSITIVE_MARGINAL_EDGE=101959
- strike_inconsistency: NO_QUOTE=495297842, LOW_VOLUME=146882588, PRELIM_GROSS_TOO_LOW=21685989, LEG_NOT_TRADABLE=8585396, OVER_CANDIDATE_CAP=256512
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
