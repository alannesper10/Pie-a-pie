# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 625 (625) | 609 (609) | 609 (609) | 45 |
| Oportunidades | 100688 | 91141 | 89496 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 100686 | 8831524 | 603959103 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.995 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05535 | 0.04306 | 0.02122 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 161.1 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=100617, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5477428, LOW_VOLUME=2378979, PRELIM_GROSS_TOO_LOW=496452, OVER_CANDIDATE_CAP=298992, NO_POSITIVE_MARGINAL_EDGE=91313
- strike_inconsistency: NO_QUOTE=445321092, LOW_VOLUME=131001426, PRELIM_GROSS_TOO_LOW=19419119, LEG_NOT_TRADABLE=7701372, OVER_CANDIDATE_CAP=225226
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
