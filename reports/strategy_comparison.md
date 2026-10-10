# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 169 (169) | 153 (153) | 153 (153) | 45 |
| Oportunidades | 26980 | 22904 | 22569 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 26980 | 2316759 | 148837886 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.156 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05483 | 0.04503 | 0.022 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 159.6 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=26980
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1441243, LOW_VOLUME=624867, PRELIM_GROSS_TOO_LOW=126537, OVER_CANDIDATE_CAP=77975, NO_POSITIVE_MARGINAL_EDGE=22941
- strike_inconsistency: NO_QUOTE=110106407, LOW_VOLUME=31590846, PRELIM_GROSS_TOO_LOW=4916204, LEG_NOT_TRADABLE=2099897, OVER_CANDIDATE_CAP=51180
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
