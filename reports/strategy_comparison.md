# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 327 (327) | 311 (311) | 311 (311) | 45 |
| Oportunidades | 55829 | 46547 | 45617 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55829 | 4516328 | 306897442 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.059 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05562 | 0.04364 | 0.02178 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.7 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55829
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2830824, LOW_VOLUME=1185912, PRELIM_GROSS_TOO_LOW=254605, OVER_CANDIDATE_CAP=148958, NO_POSITIVE_MARGINAL_EDGE=46626
- strike_inconsistency: NO_QUOTE=230539176, LOW_VOLUME=62749111, PRELIM_GROSS_TOO_LOW=9570842, LEG_NOT_TRADABLE=3794301, GROUPING_MISMATCH=101121
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
