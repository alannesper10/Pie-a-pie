# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 325 (325) | 309 (309) | 309 (309) | 45 |
| Oportunidades | 55520 | 46248 | 45317 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55520 | 4491013 | 305366698 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.061 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04365 | 0.02179 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.8 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55520
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2815109, LOW_VOLUME=1179225, PRELIM_GROSS_TOO_LOW=253103, OVER_CANDIDATE_CAP=148119, NO_POSITIVE_MARGINAL_EDGE=46326
- strike_inconsistency: NO_QUOTE=229387169, LOW_VOLUME=62434879, PRELIM_GROSS_TOO_LOW=9521460, LEG_NOT_TRADABLE=3780561, GROUPING_MISMATCH=100457
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
