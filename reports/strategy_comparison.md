# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 100 (100) | 84 (84) | 84 (84) | 45 |
| Oportunidades | 12608 | 12579 | 12421 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12608 | 1224727 | 81841677 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.186 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04533 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 126.1 | 149.8 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12608
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=753530, LOW_VOLUME=340347, PRELIM_GROSS_TOO_LOW=66347, OVER_CANDIDATE_CAP=39360, NO_POSITIVE_MARGINAL_EDGE=12596
- strike_inconsistency: NO_QUOTE=61509272, LOW_VOLUME=16638078, PRELIM_GROSS_TOO_LOW=2553524, LEG_NOT_TRADABLE=1072852, GROUPING_MISMATCH=27671
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
