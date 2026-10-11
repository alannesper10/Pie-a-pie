# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 289 (289) | 273 (273) | 273 (273) | 45 |
| Oportunidades | 50539 | 40856 | 39961 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50539 | 4042209 | 270246188 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.079 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05551 | 0.04385 | 0.02194 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 174.9 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50539
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2536216, LOW_VOLUME=1060288, PRELIM_GROSS_TOO_LOW=227836, OVER_CANDIDATE_CAP=133354, NO_POSITIVE_MARGINAL_EDGE=40927
- strike_inconsistency: NO_QUOTE=201343195, LOW_VOLUME=56394962, PRELIM_GROSS_TOO_LOW=8768348, LEG_NOT_TRADABLE=3520519, GROUPING_MISMATCH=89310
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
