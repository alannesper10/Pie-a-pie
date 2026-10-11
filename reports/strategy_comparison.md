# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 275 (275) | 259 (259) | 259 (259) | 45 |
| Oportunidades | 48716 | 38764 | 37969 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 48716 | 3864711 | 256694927 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.09 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05544 | 0.04396 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.1 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=48716
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2423579, LOW_VOLUME=1015175, PRELIM_GROSS_TOO_LOW=217621, OVER_CANDIDATE_CAP=128366, NO_POSITIVE_MARGINAL_EDGE=38834
- strike_inconsistency: NO_QUOTE=190767885, LOW_VOLUME=53864380, PRELIM_GROSS_TOO_LOW=8454539, LEG_NOT_TRADABLE=3400847, GROUPING_MISMATCH=84741
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
