# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 124 (124) | 108 (108) | 108 (108) | 45 |
| Oportunidades | 17287 | 16168 | 15965 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 17287 | 1596398 | 105965024 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.179 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05426 | 0.04522 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 139.4 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=17287
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=986309, LOW_VOLUME=439019, PRELIM_GROSS_TOO_LOW=86542, OVER_CANDIDATE_CAP=52479, NO_POSITIVE_MARGINAL_EDGE=16193
- strike_inconsistency: NO_QUOTE=79750048, LOW_VOLUME=21343040, PRELIM_GROSS_TOO_LOW=3297975, LEG_NOT_TRADABLE=1487657, GROUPING_MISMATCH=35471
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
