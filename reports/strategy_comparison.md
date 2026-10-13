# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 354 (354) | 338 (338) | 338 (338) | 45 |
| Oportunidades | 59219 | 50589 | 49620 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 59218 | 4869878 | 331182990 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05589 | 0.04353 | 0.02167 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 167.3 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=59188, SUSPICIOUS_EDGE_CHECK_RULES=30
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3046006, LOW_VOLUME=1284987, PRELIM_GROSS_TOO_LOW=274217, OVER_CANDIDATE_CAP=160725, NO_POSITIVE_MARGINAL_EDGE=50673
- strike_inconsistency: NO_QUOTE=249010390, LOW_VOLUME=67507828, PRELIM_GROSS_TOO_LOW=10251331, LEG_NOT_TRADABLE=4149273, GROUPING_MISMATCH=110151
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
