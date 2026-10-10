# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 157 (157) | 141 (141) | 141 (141) | 45 |
| Oportunidades | 24013 | 21107 | 20784 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 24013 | 2124599 | 136473705 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.164 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05467 | 0.04515 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 152.9 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=24013
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1320775, LOW_VOLUME=575148, PRELIM_GROSS_TOO_LOW=115721, OVER_CANDIDATE_CAP=70729, NO_POSITIVE_MARGINAL_EDGE=21141
- strike_inconsistency: NO_QUOTE=101118941, LOW_VOLUME=28776638, PRELIM_GROSS_TOO_LOW=4498670, LEG_NOT_TRADABLE=1963862, OVER_CANDIDATE_CAP=47966
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
