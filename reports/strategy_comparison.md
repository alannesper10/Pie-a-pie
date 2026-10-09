# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 114 (114) | 98 (98) | 98 (98) | 45 |
| Oportunidades | 15234 | 14675 | 14509 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 15234 | 1439701 | 96548420 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.188 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05413 | 0.04527 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 133.6 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=15234
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=887133, LOW_VOLUME=398226, PRELIM_GROSS_TOO_LOW=77955, OVER_CANDIDATE_CAP=47121, NO_POSITIVE_MARGINAL_EDGE=14695
- strike_inconsistency: NO_QUOTE=72878637, LOW_VOLUME=19457484, PRELIM_GROSS_TOO_LOW=2972670, LEG_NOT_TRADABLE=1161340, GROUPING_MISMATCH=32221
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
