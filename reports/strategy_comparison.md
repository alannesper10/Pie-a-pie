# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 118 (118) | 102 (102) | 102 (102) | 45 |
| Oportunidades | 16015 | 15272 | 15099 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 16015 | 1501970 | 100633057 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.189 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05416 | 0.04529 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 135.7 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=16015
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=926387, LOW_VOLUME=414652, PRELIM_GROSS_TOO_LOW=81306, OVER_CANDIDATE_CAP=49234, NO_POSITIVE_MARGINAL_EDGE=15295
- strike_inconsistency: NO_QUOTE=76039542, LOW_VOLUME=20224151, PRELIM_GROSS_TOO_LOW=3100021, LEG_NOT_TRADABLE=1187986, GROUPING_MISMATCH=33521
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
