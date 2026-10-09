# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 87 (87) | 71 (71) | 71 (71) | 45 |
| Oportunidades | 10499 | 10631 | 10519 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10499 | 1024736 | 68297341 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.196 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05408 | 0.04547 | 0.02197 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 120.7 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10499
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=629744, LOW_VOLUME=285504, PRELIM_GROSS_TOO_LOW=56026, OVER_CANDIDATE_CAP=32556, NO_POSITIVE_MARGINAL_EDGE=10646
- strike_inconsistency: NO_QUOTE=51177318, LOW_VOLUME=13896054, PRELIM_GROSS_TOO_LOW=2181379, LEG_NOT_TRADABLE=985135, GROUPING_MISMATCH=23396
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
