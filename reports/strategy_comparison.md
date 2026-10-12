# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 329 (329) | 313 (313) | 313 (313) | 45 |
| Oportunidades | 56119 | 46847 | 45912 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56119 | 4541795 | 308267793 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.057 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04362 | 0.02177 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.6 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56119
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2846603, LOW_VOLUME=1192663, PRELIM_GROSS_TOO_LOW=256124, OVER_CANDIDATE_CAP=149801, NO_POSITIVE_MARGINAL_EDGE=46926
- strike_inconsistency: NO_QUOTE=231529923, LOW_VOLUME=63062526, PRELIM_GROSS_TOO_LOW=9621135, LEG_NOT_TRADABLE=3808795, GROUPING_MISMATCH=101785
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
