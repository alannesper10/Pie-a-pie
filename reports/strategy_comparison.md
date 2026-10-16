# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 514 (514) | 498 (498) | 498 (498) | 45 |
| Oportunidades | 81447 | 74535 | 73342 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 81445 | 7190759 | 487789435 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05573 | 0.04309 | 0.02131 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 158.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=81376, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4452275, LOW_VOLUME=1940659, PRELIM_GROSS_TOO_LOW=406702, OVER_CANDIDATE_CAP=243548, NO_POSITIVE_MARGINAL_EDGE=74667
- strike_inconsistency: NO_QUOTE=362947168, LOW_VOLUME=102842406, PRELIM_GROSS_TOO_LOW=15205346, LEG_NOT_TRADABLE=6392961, OVER_CANDIDATE_CAP=163964
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
