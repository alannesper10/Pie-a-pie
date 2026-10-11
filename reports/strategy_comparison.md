# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 253 (253) | 237 (237) | 237 (237) | 45 |
| Oportunidades | 44624 | 35466 | 34787 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 44624 | 3569201 | 234564279 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.111 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05524 | 0.04423 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 176.4 | 149.6 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=44624
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2235286, LOW_VOLUME=941753, PRELIM_GROSS_TOO_LOW=199505, OVER_CANDIDATE_CAP=119499, NO_POSITIVE_MARGINAL_EDGE=35534
- strike_inconsistency: NO_QUOTE=173743299, LOW_VOLUME=49567198, PRELIM_GROSS_TOO_LOW=7818047, LEG_NOT_TRADABLE=3243634, OVER_CANDIDATE_CAP=78413
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
