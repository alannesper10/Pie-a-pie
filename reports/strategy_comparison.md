# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 708 (708) | 692 (692) | 692 (692) | 45 |
| Oportunidades | 110575 | 103569 | 101828 | 0 |
| Net-positive | 2 | 0 | 26 | 0 |
| Ejecutables | 2 | 0 | 25 | 0 |
| Descartadas | 110573 | 9980135 | 685941749 | 2412 |
| Duración media (min) | 0 | n/d | 23.07 | n/d |
| Capital por paquete (media) | 1.014 | 1.982 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04284 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.2 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110504, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6166550, LOW_VOLUME=2710066, PRELIM_GROSS_TOO_LOW=562050, OVER_CANDIDATE_CAP=339742, NO_POSITIVE_MARGINAL_EDGE=103759
- strike_inconsistency: NO_QUOTE=504722105, LOW_VOLUME=149786414, PRELIM_GROSS_TOO_LOW=22107931, LEG_NOT_TRADABLE=8734402, OVER_CANDIDATE_CAP=261176
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
