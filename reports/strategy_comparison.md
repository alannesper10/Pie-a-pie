# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 286 (286) | 270 (270) | 270 (270) | 45 |
| Oportunidades | 50163 | 40408 | 39546 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50163 | 4004907 | 267257185 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.08 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0555 | 0.04386 | 0.02196 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 175.4 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50163
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2512671, LOW_VOLUME=1050730, PRELIM_GROSS_TOO_LOW=225756, OVER_CANDIDATE_CAP=132242, NO_POSITIVE_MARGINAL_EDGE=40478
- strike_inconsistency: NO_QUOTE=198971311, LOW_VOLUME=55865168, PRELIM_GROSS_TOO_LOW=8707966, LEG_NOT_TRADABLE=3495847, GROUPING_MISMATCH=88334
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
