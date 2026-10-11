# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 276 (276) | 260 (260) | 260 (260) | 45 |
| Oportunidades | 48852 | 38914 | 38105 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 48852 | 3877810 | 257703950 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.088 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05545 | 0.04395 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=48852
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2431956, LOW_VOLUME=1018451, PRELIM_GROSS_TOO_LOW=218402, OVER_CANDIDATE_CAP=128722, NO_POSITIVE_MARGINAL_EDGE=38984
- strike_inconsistency: NO_QUOTE=191551498, LOW_VOLUME=54052196, PRELIM_GROSS_TOO_LOW=8482753, LEG_NOT_TRADABLE=3409271, GROUPING_MISMATCH=85080
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
