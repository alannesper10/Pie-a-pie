# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 797 (797) | 781 (780) | 781 (780) | 45 |
| Oportunidades | 123111 | 116738 | 114892 | 0 |
| Net-positive | 2 | 0 | 43 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 123109 | 11369282 | 775105850 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.959 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05519 | 0.04253 | 0.02111 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=123040, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7009959, LOW_VOLUME=3098020, PRELIM_GROSS_TOO_LOW=644757, OVER_CANDIDATE_CAP=389907, NO_POSITIVE_MARGINAL_EDGE=116955
- strike_inconsistency: NO_QUOTE=566260745, LOW_VOLUME=172661397, PRELIM_GROSS_TOO_LOW=25588845, LEG_NOT_TRADABLE=9912800, OVER_CANDIDATE_CAP=310887
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
