# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 125 (125) | 109 (109) | 109 (109) | 45 |
| Oportunidades | 17500 | 16318 | 16113 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 17500 | 1612229 | 106706068 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.176 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05427 | 0.0452 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 140 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=17500
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=996372, LOW_VOLUME=443081, PRELIM_GROSS_TOO_LOW=87445, OVER_CANDIDATE_CAP=53007, NO_POSITIVE_MARGINAL_EDGE=16343
- strike_inconsistency: NO_QUOTE=80263299, LOW_VOLUME=21528559, PRELIM_GROSS_TOO_LOW=3333061, LEG_NOT_TRADABLE=1493981, GROUPING_MISMATCH=35796
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
