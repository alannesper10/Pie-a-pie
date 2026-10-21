# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 716 (716) | 700 (700) | 700 (700) | 45 |
| Oportunidades | 111534 | 104763 | 103021 | 0 |
| Net-positive | 2 | 0 | 34 | 0 |
| Ejecutables | 2 | 0 | 33 | 0 |
| Descartadas | 111532 | 10097673 | 694138434 | 2412 |
| Duración media (min) | 0 | n/d | 19.35 | n/d |
| Capital por paquete (media) | 1.014 | 1.978 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05521 | 0.04278 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.8 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=111463, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6237048, LOW_VOLUME=2744110, PRELIM_GROSS_TOO_LOW=568696, OVER_CANDIDATE_CAP=344088, NO_POSITIVE_MARGINAL_EDGE=104959
- strike_inconsistency: NO_QUOTE=510681478, LOW_VOLUME=151600333, PRELIM_GROSS_TOO_LOW=22424048, LEG_NOT_TRADABLE=8834264, OVER_CANDIDATE_CAP=264945
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
