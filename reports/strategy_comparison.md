# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 649 (649) | 633 (633) | 633 (633) | 45 |
| Oportunidades | 103555 | 94736 | 93055 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 103553 | 9141208 | 625987956 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.991 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05531 | 0.04299 | 0.02121 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 159.6 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=103484, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5667596, LOW_VOLUME=2464490, PRELIM_GROSS_TOO_LOW=513615, OVER_CANDIDATE_CAP=309519, NO_POSITIVE_MARGINAL_EDGE=94913
- strike_inconsistency: NO_QUOTE=461597106, LOW_VOLUME=135753776, PRELIM_GROSS_TOO_LOW=20104357, LEG_NOT_TRADABLE=7997674, OVER_CANDIDATE_CAP=233029
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
