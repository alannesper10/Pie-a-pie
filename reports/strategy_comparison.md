# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 188 (188) | 172 (172) | 172 (172) | 45 |
| Oportunidades | 31572 | 25746 | 25403 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 31572 | 2619008 | 168692408 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.142 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04476 | 0.02213 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 167.9 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=31572
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1633249, LOW_VOLUME=701076, PRELIM_GROSS_TOO_LOW=143714, OVER_CANDIDATE_CAP=88961, NO_POSITIVE_MARGINAL_EDGE=25789
- strike_inconsistency: NO_QUOTE=124432940, LOW_VOLUME=35984497, PRELIM_GROSS_TOO_LOW=5624465, LEG_NOT_TRADABLE=2511237, OVER_CANDIDATE_CAP=56854
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
