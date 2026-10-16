# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 505 (505) | 489 (489) | 489 (489) | 45 |
| Oportunidades | 79597 | 73187 | 71997 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 79595 | 7045488 | 480722676 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.002 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05576 | 0.04311 | 0.02133 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 157.6 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=79526, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4360692, LOW_VOLUME=1903120, PRELIM_GROSS_TOO_LOW=398556, OVER_CANDIDATE_CAP=237988, NO_POSITIVE_MARGINAL_EDGE=73317
- strike_inconsistency: NO_QUOTE=358530815, LOW_VOLUME=100630025, PRELIM_GROSS_TOO_LOW=14858143, LEG_NOT_TRADABLE=6312620, GROUPING_MISMATCH=158924
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
