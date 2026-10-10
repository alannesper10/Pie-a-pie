# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 195 (195) | 179 (179) | 179 (179) | 45 |
| Oportunidades | 33082 | 26792 | 26442 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 33082 | 2728686 | 176051926 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.136 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04467 | 0.02219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 169.7 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=33082
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1703508, LOW_VOLUME=727906, PRELIM_GROSS_TOO_LOW=150155, OVER_CANDIDATE_CAP=92825, NO_POSITIVE_MARGINAL_EDGE=26839
- strike_inconsistency: NO_QUOTE=129764232, LOW_VOLUME=37557573, PRELIM_GROSS_TOO_LOW=5921137, LEG_NOT_TRADABLE=2663954, OVER_CANDIDATE_CAP=59262
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
