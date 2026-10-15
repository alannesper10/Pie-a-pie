# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 474 (474) | 458 (458) | 458 (458) | 45 |
| Oportunidades | 74194 | 68546 | 67407 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 74192 | 6564097 | 447937771 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.007 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0558 | 0.04314 | 0.02139 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.5 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=74123, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4062939, LOW_VOLUME=1771982, PRELIM_GROSS_TOO_LOW=371978, OVER_CANDIDATE_CAP=220760, NO_POSITIVE_MARGINAL_EDGE=68668
- strike_inconsistency: NO_QUOTE=335115616, LOW_VOLUME=92856667, PRELIM_GROSS_TOO_LOW=13807731, LEG_NOT_TRADABLE=5794815, GROUPING_MISMATCH=148978
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
