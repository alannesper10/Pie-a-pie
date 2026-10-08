# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 43 (43) | 27 (27) | 27 (27) | 45 |
| Oportunidades | 4720 | 4044 | 4001 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4720 | 378561 | 27126971 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.526 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04873 | 0.02195 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.8 | 149.8 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4720
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=229423, LOW_VOLUME=107794, PRELIM_GROSS_TOO_LOW=21437, OVER_CANDIDATE_CAP=11678, NO_POSITIVE_MARGINAL_EDGE=4048
- strike_inconsistency: NO_QUOTE=20988297, LOW_VOLUME=5162979, PRELIM_GROSS_TOO_LOW=794693, LEG_NOT_TRADABLE=159979, GROUPING_MISMATCH=8895
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
