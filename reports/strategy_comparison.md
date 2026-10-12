# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 332 (332) | 316 (316) | 316 (316) | 45 |
| Oportunidades | 56541 | 47297 | 46361 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56541 | 4579989 | 310000947 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.056 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05564 | 0.04361 | 0.02175 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.3 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56538, SUSPICIOUS_EDGE_CHECK_RULES=3
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2870220, LOW_VOLUME=1202893, PRELIM_GROSS_TOO_LOW=258366, OVER_CANDIDATE_CAP=151098, NO_POSITIVE_MARGINAL_EDGE=47376
- strike_inconsistency: NO_QUOTE=232699774, LOW_VOLUME=63528267, PRELIM_GROSS_TOO_LOW=9695250, LEG_NOT_TRADABLE=3830046, GROUPING_MISMATCH=102781
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
