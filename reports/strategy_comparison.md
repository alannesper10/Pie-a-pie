# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 277 (277) | 261 (261) | 261 (261) | 45 |
| Oportunidades | 48992 | 39064 | 38236 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 48992 | 3890849 | 258712799 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.087 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05545 | 0.04394 | 0.02201 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 176.9 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=48992
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2440302, LOW_VOLUME=1021697, PRELIM_GROSS_TOO_LOW=219171, OVER_CANDIDATE_CAP=129077, NO_POSITIVE_MARGINAL_EDGE=39134
- strike_inconsistency: NO_QUOTE=192336932, LOW_VOLUME=54238929, PRELIM_GROSS_TOO_LOW=8509504, LEG_NOT_TRADABLE=3418256, GROUPING_MISMATCH=85425
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
