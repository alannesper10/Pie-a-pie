# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 426 (426) | 410 (410) | 410 (410) | 45 |
| Oportunidades | 68047 | 61364 | 60323 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 68045 | 5858391 | 401155598 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.023 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05602 | 0.04326 | 0.02146 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.7 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=67976, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3637834, LOW_VOLUME=1568471, PRELIM_GROSS_TOO_LOW=331948, OVER_CANDIDATE_CAP=197344, NO_POSITIVE_MARGINAL_EDGE=61470
- strike_inconsistency: NO_QUOTE=302041336, LOW_VOLUME=81134297, PRELIM_GROSS_TOO_LOW=12222057, LEG_NOT_TRADABLE=5436183, GROUPING_MISMATCH=133475
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
