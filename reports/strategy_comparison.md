# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 44 (44) | 28 (28) | 28 (28) | 45 |
| Oportunidades | 4813 | 4194 | 4151 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4813 | 392580 | 28168270 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.512 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.0545 | 0.04858 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.4 | 149.8 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4813
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=237916, LOW_VOLUME=111819, PRELIM_GROSS_TOO_LOW=22296, OVER_CANDIDATE_CAP=12044, NO_POSITIVE_MARGINAL_EDGE=4198
- strike_inconsistency: NO_QUOTE=21800105, LOW_VOLUME=5357488, PRELIM_GROSS_TOO_LOW=823120, LEG_NOT_TRADABLE=165839, GROUPING_MISMATCH=9220
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
