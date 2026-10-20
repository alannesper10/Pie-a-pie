# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 680 (680) | 664 (664) | 664 (664) | 45 |
| Oportunidades | 107306 | 99377 | 97663 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 107304 | 9569882 | 657680162 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.987 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05525 | 0.04291 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 157.8 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=107235, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5922736, LOW_VOLUME=2588600, PRELIM_GROSS_TOO_LOW=539081, OVER_CANDIDATE_CAP=325207, NO_POSITIVE_MARGINAL_EDGE=99559
- strike_inconsistency: NO_QUOTE=485067972, LOW_VOLUME=142592731, PRELIM_GROSS_TOO_LOW=21074697, LEG_NOT_TRADABLE=8384191, OVER_CANDIDATE_CAP=243979
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
