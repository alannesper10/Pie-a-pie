# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 266 (266) | 250 (250) | 250 (250) | 45 |
| Oportunidades | 47297 | 37415 | 36706 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 47297 | 3745838 | 247629713 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.099 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05538 | 0.04409 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.8 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=47297
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2347723, LOW_VOLUME=985669, PRELIM_GROSS_TOO_LOW=210250, OVER_CANDIDATE_CAP=124993, NO_POSITIVE_MARGINAL_EDGE=37484
- strike_inconsistency: NO_QUOTE=183759056, LOW_VOLUME=52155625, PRELIM_GROSS_TOO_LOW=8182035, LEG_NOT_TRADABLE=3332647, GROUPING_MISMATCH=81822
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
