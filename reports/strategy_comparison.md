# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 288 (288) | 272 (272) | 272 (272) | 45 |
| Oportunidades | 50415 | 40706 | 39831 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50415 | 4029793 | 269250668 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.08 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0555 | 0.04385 | 0.02195 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 175.1 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50415
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2528384, LOW_VOLUME=1057100, PRELIM_GROSS_TOO_LOW=227158, OVER_CANDIDATE_CAP=132975, NO_POSITIVE_MARGINAL_EDGE=40777
- strike_inconsistency: NO_QUOTE=200550629, LOW_VOLUME=56220065, PRELIM_GROSS_TOO_LOW=8749301, LEG_NOT_TRADABLE=3512201, GROUPING_MISMATCH=88987
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
