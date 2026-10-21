# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 725 (725) | 709 (709) | 709 (709) | 45 |
| Oportunidades | 112668 | 106107 | 104362 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 112666 | 10232841 | 701646358 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.975 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0552 | 0.04272 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.4 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=112597, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6319014, LOW_VOLUME=2782078, PRELIM_GROSS_TOO_LOW=576705, OVER_CANDIDATE_CAP=348935, NO_POSITIVE_MARGINAL_EDGE=106308
- strike_inconsistency: NO_QUOTE=515541059, LOW_VOLUME=153750063, PRELIM_GROSS_TOO_LOW=22800147, LEG_NOT_TRADABLE=8947830, OVER_CANDIDATE_CAP=269547
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
