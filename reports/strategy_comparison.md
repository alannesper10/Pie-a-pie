# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 257 (257) | 241 (241) | 241 (241) | 45 |
| Oportunidades | 45497 | 36066 | 35383 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 45497 | 3624249 | 238581480 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.106 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05529 | 0.04417 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 177 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=45497
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2270269, LOW_VOLUME=955544, PRELIM_GROSS_TOO_LOW=202895, OVER_CANDIDATE_CAP=121207, NO_POSITIVE_MARGINAL_EDGE=36134
- strike_inconsistency: NO_QUOTE=176809818, LOW_VOLUME=50380548, PRELIM_GROSS_TOO_LOW=7925945, LEG_NOT_TRADABLE=3270612, OVER_CANDIDATE_CAP=78964
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
