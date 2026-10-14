# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 412 (412) | 396 (396) | 396 (396) | 45 |
| Oportunidades | 66251 | 59270 | 58248 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 66249 | 5662670 | 387363850 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.026 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05608 | 0.0433 | 0.02149 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 160.8 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=66180, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3520806, LOW_VOLUME=1512394, PRELIM_GROSS_TOO_LOW=319926, OVER_CANDIDATE_CAP=190239, NO_POSITIVE_MARGINAL_EDGE=59371
- strike_inconsistency: NO_QUOTE=291683786, LOW_VOLUME=78422171, PRELIM_GROSS_TOO_LOW=11785009, LEG_NOT_TRADABLE=5162123, GROUPING_MISMATCH=129044
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
