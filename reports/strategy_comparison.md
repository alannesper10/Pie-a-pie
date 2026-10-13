# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 364 (364) | 348 (348) | 348 (348) | 45 |
| Oportunidades | 60390 | 52087 | 51112 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 60389 | 5004910 | 341381284 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.046 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05602 | 0.04354 | 0.02163 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.9 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60343, SUSPICIOUS_EDGE_CHECK_RULES=46
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3126141, LOW_VOLUME=1324254, PRELIM_GROSS_TOO_LOW=281723, OVER_CANDIDATE_CAP=166184, NO_POSITIVE_MARGINAL_EDGE=52173
- strike_inconsistency: NO_QUOTE=256909495, LOW_VOLUME=69325974, PRELIM_GROSS_TOO_LOW=10489890, LEG_NOT_TRADABLE=4384241, GROUPING_MISMATCH=113479
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
