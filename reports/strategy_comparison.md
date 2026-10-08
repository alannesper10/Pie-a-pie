# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 54 (54) | 38 (38) | 38 (38) | 45 |
| Oportunidades | 5974 | 5692 | 5632 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5974 | 532602 | 38514973 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.373 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05437 | 0.04713 | 0.02247 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 110.6 | 149.8 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5974
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=323406, LOW_VOLUME=151299, PRELIM_GROSS_TOO_LOW=30092, OVER_CANDIDATE_CAP=16503, NO_POSITIVE_MARGINAL_EDGE=5698
- strike_inconsistency: NO_QUOTE=29776403, LOW_VOLUME=7317673, PRELIM_GROSS_TOO_LOW=1122032, LEG_NOT_TRADABLE=269455, GROUPING_MISMATCH=12470
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
