# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 260 (260) | 244 (244) | 244 (244) | 45 |
| Oportunidades | 46127 | 36516 | 35824 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 46127 | 3665150 | 241598912 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.103 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05532 | 0.04414 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.4 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=46127
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2296358, LOW_VOLUME=965702, PRELIM_GROSS_TOO_LOW=205300, OVER_CANDIDATE_CAP=122508, NO_POSITIVE_MARGINAL_EDGE=36584
- strike_inconsistency: NO_QUOTE=179121804, LOW_VOLUME=50981081, PRELIM_GROSS_TOO_LOW=8008495, LEG_NOT_TRADABLE=3291076, GROUPING_MISMATCH=79933
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
