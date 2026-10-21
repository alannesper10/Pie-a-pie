# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 713 (713) | 697 (697) | 697 (697) | 45 |
| Oportunidades | 111176 | 104316 | 102575 | 0 |
| Net-positive | 2 | 0 | 31 | 0 |
| Ejecutables | 2 | 0 | 30 | 0 |
| Descartadas | 111174 | 10053573 | 691324567 | 2412 |
| Duración media (min) | 0 | n/d | 19.7 | n/d |
| Capital por paquete (media) | 1.014 | 1.98 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.0428 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.9 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=111105, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6210462, LOW_VOLUME=2731516, PRELIM_GROSS_TOO_LOW=566185, OVER_CANDIDATE_CAP=342432, NO_POSITIVE_MARGINAL_EDGE=104509
- strike_inconsistency: NO_QUOTE=508669756, LOW_VOLUME=150962476, PRELIM_GROSS_TOO_LOW=22300021, LEG_NOT_TRADABLE=8796995, OVER_CANDIDATE_CAP=263323
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
