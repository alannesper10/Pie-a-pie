# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 127 (127) | 111 (111) | 111 (111) | 45 |
| Oportunidades | 17933 | 16617 | 16402 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 17933 | 1643891 | 108189575 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.174 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05429 | 0.04518 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 141.2 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=17933
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1016495, LOW_VOLUME=451181, PRELIM_GROSS_TOO_LOW=89210, OVER_CANDIDATE_CAP=54092, NO_POSITIVE_MARGINAL_EDGE=16643
- strike_inconsistency: NO_QUOTE=81293191, LOW_VOLUME=21896704, PRELIM_GROSS_TOO_LOW=3402570, LEG_NOT_TRADABLE=1508118, GROUPING_MISMATCH=36446
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
