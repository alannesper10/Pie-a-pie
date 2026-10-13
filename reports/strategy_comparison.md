# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 373 (373) | 357 (357) | 357 (357) | 45 |
| Oportunidades | 61492 | 53434 | 52459 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61490 | 5125582 | 350610615 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.043 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05609 | 0.0435 | 0.0216 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 164.9 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61436, SUSPICIOUS_EDGE_CHECK_RULES=54
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3198302, LOW_VOLUME=1358683, PRELIM_GROSS_TOO_LOW=288755, OVER_CANDIDATE_CAP=170913, NO_POSITIVE_MARGINAL_EDGE=53523
- strike_inconsistency: NO_QUOTE=264245244, LOW_VOLUME=70929800, PRELIM_GROSS_TOO_LOW=10710406, LEG_NOT_TRADABLE=4446540, GROUPING_MISMATCH=116458
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
