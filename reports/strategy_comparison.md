# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 388 (388) | 372 (372) | 372 (372) | 45 |
| Oportunidades | 63354 | 55678 | 54686 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 63352 | 5327660 | 363412953 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.035 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05617 | 0.04339 | 0.02155 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 163.3 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=63283, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3321117, LOW_VOLUME=1414867, PRELIM_GROSS_TOO_LOW=300382, OVER_CANDIDATE_CAP=178309, NO_POSITIVE_MARGINAL_EDGE=55773
- strike_inconsistency: NO_QUOTE=273857799, LOW_VOLUME=73519965, PRELIM_GROSS_TOO_LOW=11096667, LEG_NOT_TRADABLE=4647461, GROUPING_MISMATCH=121376
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
