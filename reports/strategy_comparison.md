# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 706 (706) | 690 (690) | 690 (690) | 45 |
| Oportunidades | 110328 | 103269 | 101528 | 0 |
| Net-positive | 2 | 0 | 24 | 0 |
| Ejecutables | 2 | 0 | 23 | 0 |
| Descartadas | 110326 | 9950657 | 683776109 | 2412 |
| Duración media (min) | 0 | n/d | 22.02 | n/d |
| Capital por paquete (media) | 1.014 | 1.982 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04285 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.3 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110257, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6149098, LOW_VOLUME=2701365, PRELIM_GROSS_TOO_LOW=560276, OVER_CANDIDATE_CAP=338676, NO_POSITIVE_MARGINAL_EDGE=103459
- strike_inconsistency: NO_QUOTE=503127947, LOW_VOLUME=149311988, PRELIM_GROSS_TOO_LOW=22037269, LEG_NOT_TRADABLE=8709731, OVER_CANDIDATE_CAP=260371
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
