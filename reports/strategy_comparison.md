# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 313 (313) | 297 (297) | 297 (297) | 45 |
| Oportunidades | 53729 | 44451 | 43523 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 53729 | 4341426 | 294078869 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.069 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04372 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.7 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=53729
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2721798, LOW_VOLUME=1139964, PRELIM_GROSS_TOO_LOW=244423, OVER_CANDIDATE_CAP=143229, NO_POSITIVE_MARGINAL_EDGE=44526
- strike_inconsistency: NO_QUOTE=220411326, LOW_VOLUME=60494175, PRELIM_GROSS_TOO_LOW=9246490, LEG_NOT_TRADABLE=3692021, GROUPING_MISMATCH=96726
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
