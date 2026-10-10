# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 190 (190) | 174 (174) | 174 (174) | 45 |
| Oportunidades | 32027 | 26044 | 25703 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 32027 | 2650727 | 170795068 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.14 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05493 | 0.04473 | 0.02215 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 168.6 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=32027
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1653578, LOW_VOLUME=708809, PRELIM_GROSS_TOO_LOW=145553, OVER_CANDIDATE_CAP=90098, NO_POSITIVE_MARGINAL_EDGE=26089
- strike_inconsistency: NO_QUOTE=125954968, LOW_VOLUME=36437773, PRELIM_GROSS_TOO_LOW=5706516, LEG_NOT_TRADABLE=2554916, OVER_CANDIDATE_CAP=57526
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
