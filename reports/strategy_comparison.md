# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 434 (434) | 418 (418) | 418 (418) | 45 |
| Oportunidades | 69017 | 62561 | 61515 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 69015 | 5972439 | 408178199 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.021 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05598 | 0.04324 | 0.02145 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=68946, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3706796, LOW_VOLUME=1600921, PRELIM_GROSS_TOO_LOW=338362, OVER_CANDIDATE_CAP=201396, NO_POSITIVE_MARGINAL_EDGE=62670
- strike_inconsistency: NO_QUOTE=307011316, LOW_VOLUME=82867932, PRELIM_GROSS_TOO_LOW=12473756, LEG_NOT_TRADABLE=5496770, GROUPING_MISMATCH=136207
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
