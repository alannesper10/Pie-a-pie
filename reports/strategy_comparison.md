# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 886 (886) | 870 (869) | 870 (869) | 45 |
| Oportunidades | 139355 | 130056 | 127948 | 0 |
| Net-positive | 2 | 0 | 44 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 139353 | 12885147 | 878308386 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.942 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0551 | 0.04223 | 0.02106 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 157.3 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=139284, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7877054, LOW_VOLUME=3575739, PRELIM_GROSS_TOO_LOW=729255, OVER_CANDIDATE_CAP=446451, NO_POSITIVE_MARGINAL_EDGE=130299
- strike_inconsistency: NO_QUOTE=637287828, LOW_VOLUME=199299487, PRELIM_GROSS_TOO_LOW=29039897, LEG_NOT_TRADABLE=11912446, OVER_CANDIDATE_CAP=354241
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
