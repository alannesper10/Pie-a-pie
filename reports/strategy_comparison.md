# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 375 (375) | 359 (359) | 359 (359) | 45 |
| Oportunidades | 61738 | 53734 | 52759 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61736 | 5152307 | 352605337 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.042 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0561 | 0.04349 | 0.02159 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 164.6 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61680, SUSPICIOUS_EDGE_CHECK_RULES=56
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3214426, LOW_VOLUME=1366207, PRELIM_GROSS_TOO_LOW=290258, OVER_CANDIDATE_CAP=171949, NO_POSITIVE_MARGINAL_EDGE=53823
- strike_inconsistency: NO_QUOTE=265724540, LOW_VOLUME=71287092, PRELIM_GROSS_TOO_LOW=10760307, LEG_NOT_TRADABLE=4553202, GROUPING_MISMATCH=117120
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
