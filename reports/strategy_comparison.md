# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 335 (335) | 319 (319) | 319 (319) | 45 |
| Oportunidades | 56964 | 47747 | 46809 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56964 | 4618698 | 311909724 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.054 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05566 | 0.0436 | 0.02174 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56958, SUSPICIOUS_EDGE_CHECK_RULES=6
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2894069, LOW_VOLUME=1213447, PRELIM_GROSS_TOO_LOW=260557, OVER_CANDIDATE_CAP=152371, NO_POSITIVE_MARGINAL_EDGE=47826
- strike_inconsistency: NO_QUOTE=234014669, LOW_VOLUME=64024822, PRELIM_GROSS_TOO_LOW=9769564, LEG_NOT_TRADABLE=3850924, GROUPING_MISMATCH=103777
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
