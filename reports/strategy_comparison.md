# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 429 (429) | 413 (413) | 413 (413) | 45 |
| Oportunidades | 68418 | 61812 | 60767 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 68416 | 5901189 | 403136358 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.022 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05601 | 0.04325 | 0.02145 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.5 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=68347, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3663668, LOW_VOLUME=1580619, PRELIM_GROSS_TOO_LOW=334419, OVER_CANDIDATE_CAP=198890, NO_POSITIVE_MARGINAL_EDGE=61920
- strike_inconsistency: NO_QUOTE=303347336, LOW_VOLUME=81687816, PRELIM_GROSS_TOO_LOW=12317129, LEG_NOT_TRADABLE=5459830, GROUPING_MISMATCH=134530
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
