# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 336 (336) | 320 (320) | 320 (320) | 45 |
| Oportunidades | 57092 | 47897 | 46959 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57092 | 4631612 | 312770846 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.053 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05567 | 0.04359 | 0.02174 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.9 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57085, SUSPICIOUS_EDGE_CHECK_RULES=7
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2902014, LOW_VOLUME=1217002, PRELIM_GROSS_TOO_LOW=261256, OVER_CANDIDATE_CAP=152796, NO_POSITIVE_MARGINAL_EDGE=47976
- strike_inconsistency: NO_QUOTE=234658815, LOW_VOLUME=64208501, PRELIM_GROSS_TOO_LOW=9795033, LEG_NOT_TRADABLE=3858026, GROUPING_MISMATCH=104109
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
