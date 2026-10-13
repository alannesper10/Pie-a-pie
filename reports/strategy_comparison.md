# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 383 (383) | 367 (367) | 367 (367) | 45 |
| Oportunidades | 62732 | 54932 | 53945 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 62730 | 5259354 | 359957545 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.037 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05615 | 0.04342 | 0.02157 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 163.8 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=62665, SUSPICIOUS_EDGE_CHECK_RULES=65
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3279499, LOW_VOLUME=1395876, PRELIM_GROSS_TOO_LOW=296399, OVER_CANDIDATE_CAP=175945, NO_POSITIVE_MARGINAL_EDGE=55023
- strike_inconsistency: NO_QUOTE=271431075, LOW_VOLUME=72662747, PRELIM_GROSS_TOO_LOW=10965291, LEG_NOT_TRADABLE=4612055, GROUPING_MISMATCH=119696
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
