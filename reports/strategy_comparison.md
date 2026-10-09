# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 134 (134) | 118 (118) | 118 (118) | 45 |
| Oportunidades | 19286 | 17662 | 17445 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 19286 | 1755168 | 112806774 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.178 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05436 | 0.04527 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 143.9 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=19286
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1087135, LOW_VOLUME=480012, PRELIM_GROSS_TOO_LOW=95338, OVER_CANDIDATE_CAP=57713, NO_POSITIVE_MARGINAL_EDGE=17691
- strike_inconsistency: NO_QUOTE=84038986, LOW_VOLUME=23217251, PRELIM_GROSS_TOO_LOW=3639961, LEG_NOT_TRADABLE=1816086, GROUPING_MISMATCH=38721
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
