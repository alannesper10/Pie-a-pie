# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 385 (385) | 369 (369) | 369 (369) | 45 |
| Oportunidades | 62989 | 55232 | 54243 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 62987 | 5286410 | 361398973 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.037 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05618 | 0.04341 | 0.02156 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 163.6 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=62918, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3295983, LOW_VOLUME=1403364, PRELIM_GROSS_TOO_LOW=297994, OVER_CANDIDATE_CAP=176888, NO_POSITIVE_MARGINAL_EDGE=55323
- strike_inconsistency: NO_QUOTE=272463151, LOW_VOLUME=73003391, PRELIM_GROSS_TOO_LOW=11018083, LEG_NOT_TRADABLE=4626093, GROUPING_MISMATCH=120346
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
