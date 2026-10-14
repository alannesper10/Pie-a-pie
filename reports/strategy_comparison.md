# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 424 (424) | 408 (408) | 408 (408) | 45 |
| Oportunidades | 67794 | 61066 | 60030 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 67792 | 5829973 | 399543846 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.024 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05603 | 0.04327 | 0.02146 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.9 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=67723, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3620701, LOW_VOLUME=1560433, PRELIM_GROSS_TOO_LOW=330258, OVER_CANDIDATE_CAP=196289, NO_POSITIVE_MARGINAL_EDGE=61171
- strike_inconsistency: NO_QUOTE=300881861, LOW_VOLUME=80763268, PRELIM_GROSS_TOO_LOW=12157580, LEG_NOT_TRADABLE=5421116, GROUPING_MISMATCH=132819
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
