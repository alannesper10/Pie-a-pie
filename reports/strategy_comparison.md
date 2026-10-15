# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 453 (453) | 437 (437) | 437 (437) | 45 |
| Oportunidades | 71073 | 65407 | 64290 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 71071 | 6250155 | 428120207 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.015 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0559 | 0.0432 | 0.02143 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.9 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=71002, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3872051, LOW_VOLUME=1683008, PRELIM_GROSS_TOO_LOW=354370, OVER_CANDIDATE_CAP=210294, NO_POSITIVE_MARGINAL_EDGE=65519
- strike_inconsistency: NO_QUOTE=321260844, LOW_VOLUME=87753795, PRELIM_GROSS_TOO_LOW=13122101, LEG_NOT_TRADABLE=5638732, GROUPING_MISMATCH=142319
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
