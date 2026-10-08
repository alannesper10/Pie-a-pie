# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 57 (57) | 41 (41) | 41 (41) | 45 |
| Oportunidades | 6329 | 6140 | 6079 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 6329 | 575138 | 41517853 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.348 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05432 | 0.04687 | 0.02251 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 111 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=6329
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=349589, LOW_VOLUME=163158, PRELIM_GROSS_TOO_LOW=32406, OVER_CANDIDATE_CAP=17869, NO_POSITIVE_MARGINAL_EDGE=6147
- strike_inconsistency: NO_QUOTE=32096655, LOW_VOLUME=7888529, PRELIM_GROSS_TOO_LOW=1214477, LEG_NOT_TRADABLE=286593, GROUPING_MISMATCH=13445
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
