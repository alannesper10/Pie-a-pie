# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 377 (377) | 361 (361) | 361 (361) | 45 |
| Oportunidades | 61989 | 54034 | 53058 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61987 | 5178996 | 354680491 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.041 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05611 | 0.04347 | 0.02158 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 164.4 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61929, SUSPICIOUS_EDGE_CHECK_RULES=58
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3230615, LOW_VOLUME=1373644, PRELIM_GROSS_TOO_LOW=291750, OVER_CANDIDATE_CAP=172972, NO_POSITIVE_MARGINAL_EDGE=54123
- strike_inconsistency: NO_QUOTE=267384613, LOW_VOLUME=71634251, PRELIM_GROSS_TOO_LOW=10811441, LEG_NOT_TRADABLE=4568421, GROUPING_MISMATCH=117782
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
