# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 707 (707) | 691 (691) | 691 (691) | 45 |
| Oportunidades | 110449 | 103419 | 101678 | 0 |
| Net-positive | 2 | 0 | 25 | 0 |
| Ejecutables | 2 | 0 | 24 | 0 |
| Descartadas | 110447 | 9965406 | 684858900 | 2412 |
| Duración media (min) | 0 | n/d | 22.02 | n/d |
| Capital por paquete (media) | 1.014 | 1.982 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04285 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.2 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110378, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6157824, LOW_VOLUME=2705720, PRELIM_GROSS_TOO_LOW=561169, OVER_CANDIDATE_CAP=339206, NO_POSITIVE_MARGINAL_EDGE=103609
- strike_inconsistency: NO_QUOTE=503925471, LOW_VOLUME=149548605, PRELIM_GROSS_TOO_LOW=22072724, LEG_NOT_TRADABLE=8722072, OVER_CANDIDATE_CAP=260766
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
