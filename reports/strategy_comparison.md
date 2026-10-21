# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 723 (723) | 707 (707) | 707 (707) | 45 |
| Oportunidades | 112412 | 105810 | 104062 | 0 |
| Net-positive | 2 | 0 | 41 | 0 |
| Ejecutables | 2 | 0 | 40 | 0 |
| Descartadas | 112410 | 10202602 | 699464178 | 2412 |
| Duración media (min) | 0 | n/d | 18.82 | n/d |
| Capital por paquete (media) | 1.014 | 1.975 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0552 | 0.04273 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.5 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=112341, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6300722, LOW_VOLUME=2773543, PRELIM_GROSS_TOO_LOW=574911, OVER_CANDIDATE_CAP=347849, NO_POSITIVE_MARGINAL_EDGE=106009
- strike_inconsistency: NO_QUOTE=514014619, LOW_VOLUME=153206529, PRELIM_GROSS_TOO_LOW=22714908, LEG_NOT_TRADABLE=8922849, OVER_CANDIDATE_CAP=268500
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
