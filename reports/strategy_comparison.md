# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 659 (659) | 643 (643) | 643 (643) | 45 |
| Oportunidades | 104647 | 96235 | 94533 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 104645 | 9277944 | 636594873 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.989 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05529 | 0.04296 | 0.0212 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 158.8 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=104576, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5749091, LOW_VOLUME=2504142, PRELIM_GROSS_TOO_LOW=521561, OVER_CANDIDATE_CAP=314290, NO_POSITIVE_MARGINAL_EDGE=96413
- strike_inconsistency: NO_QUOTE=469423063, LOW_VOLUME=138102781, PRELIM_GROSS_TOO_LOW=20401498, LEG_NOT_TRADABLE=8123897, OVER_CANDIDATE_CAP=236900
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
