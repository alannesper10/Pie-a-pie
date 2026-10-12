# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 305 (305) | 289 (289) | 289 (289) | 45 |
| Oportunidades | 52579 | 43254 | 42323 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52579 | 4242202 | 286153084 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.073 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05558 | 0.04377 | 0.02187 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.4 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52579
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2660193, LOW_VOLUME=1113697, PRELIM_GROSS_TOO_LOW=238763, OVER_CANDIDATE_CAP=139842, NO_POSITIVE_MARGINAL_EDGE=43326
- strike_inconsistency: NO_QUOTE=214059874, LOW_VOLUME=59146691, PRELIM_GROSS_TOO_LOW=9080373, LEG_NOT_TRADABLE=3636471, GROUPING_MISMATCH=94254
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
