# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 431 (431) | 415 (415) | 415 (415) | 45 |
| Oportunidades | 68659 | 62112 | 61067 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 68657 | 5929735 | 404979401 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.022 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.056 | 0.04325 | 0.02145 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.3 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=68588, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3680992, LOW_VOLUME=1588701, PRELIM_GROSS_TOO_LOW=336027, OVER_CANDIDATE_CAP=199873, NO_POSITIVE_MARGINAL_EDGE=62220
- strike_inconsistency: NO_QUOTE=304664089, LOW_VOLUME=82137053, PRELIM_GROSS_TOO_LOW=12378209, LEG_NOT_TRADABLE=5474101, GROUPING_MISMATCH=135236
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
