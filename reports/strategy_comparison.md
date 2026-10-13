# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 348 (348) | 332 (332) | 332 (332) | 45 |
| Oportunidades | 58535 | 49692 | 48738 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 58535 | 4788432 | 325003223 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05579 | 0.04353 | 0.0217 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 168.2 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=58516, SUSPICIOUS_EDGE_CHECK_RULES=19
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2997547, LOW_VOLUME=1260928, PRELIM_GROSS_TOO_LOW=269905, OVER_CANDIDATE_CAP=157946, NO_POSITIVE_MARGINAL_EDGE=49775
- strike_inconsistency: NO_QUOTE=244124547, LOW_VOLUME=66406602, PRELIM_GROSS_TOO_LOW=10107832, LEG_NOT_TRADABLE=4105030, GROUPING_MISMATCH=108101
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
