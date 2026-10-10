# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 205 (205) | 189 (189) | 189 (189) | 45 |
| Oportunidades | 35032 | 28289 | 27852 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 35032 | 2882465 | 186541818 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05492 | 0.04467 | 0.02214 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.9 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=35032
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1801843, LOW_VOLUME=765789, PRELIM_GROSS_TOO_LOW=159237, OVER_CANDIDATE_CAP=98003, NO_POSITIVE_MARGINAL_EDGE=28339
- strike_inconsistency: NO_QUOTE=137416366, LOW_VOLUME=39723945, PRELIM_GROSS_TOO_LOW=6358405, LEG_NOT_TRADABLE=2887496, OVER_CANDIDATE_CAP=64998
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
