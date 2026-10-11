# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 258 (258) | 242 (242) | 242 (242) | 45 |
| Oportunidades | 45711 | 36216 | 35532 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 45711 | 3637949 | 239587413 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.105 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0553 | 0.04415 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.2 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=45711
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2279001, LOW_VOLUME=958953, PRELIM_GROSS_TOO_LOW=203718, OVER_CANDIDATE_CAP=121636, NO_POSITIVE_MARGINAL_EDGE=36284
- strike_inconsistency: NO_QUOTE=177578510, LOW_VOLUME=50583238, PRELIM_GROSS_TOO_LOW=7952990, LEG_NOT_TRADABLE=3277494, GROUPING_MISMATCH=79285
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
