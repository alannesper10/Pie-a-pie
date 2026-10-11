# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 273 (273) | 257 (257) | 257 (257) | 45 |
| Oportunidades | 48431 | 38464 | 37715 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 48431 | 3838669 | 254685364 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.091 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05543 | 0.04398 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.4 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=48431
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2406963, LOW_VOLUME=1008671, PRELIM_GROSS_TOO_LOW=216063, OVER_CANDIDATE_CAP=127617, NO_POSITIVE_MARGINAL_EDGE=38534
- strike_inconsistency: NO_QUOTE=189200990, LOW_VOLUME=53498386, PRELIM_GROSS_TOO_LOW=8396016, LEG_NOT_TRADABLE=3384521, GROUPING_MISMATCH=84075
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
