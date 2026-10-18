# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 602 (602) | 586 (586) | 586 (586) | 45 |
| Oportunidades | 98160 | 87695 | 86282 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 98158 | 8536439 | 580476798 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.993 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05539 | 0.04305 | 0.02123 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 163.1 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=98089, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5294991, LOW_VOLUME=2298332, PRELIM_GROSS_TOO_LOW=480702, OVER_CANDIDATE_CAP=289868, NO_POSITIVE_MARGINAL_EDGE=87863
- strike_inconsistency: NO_QUOTE=427812206, LOW_VOLUME=126120938, PRELIM_GROSS_TOO_LOW=18806509, LEG_NOT_TRADABLE=7240275, OVER_CANDIDATE_CAP=216686
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
