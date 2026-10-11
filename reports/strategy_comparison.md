# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 268 (268) | 252 (252) | 252 (252) | 45 |
| Oportunidades | 47661 | 37714 | 37002 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 47661 | 3772549 | 249647097 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.097 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0554 | 0.04406 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.8 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=47661
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2364751, LOW_VOLUME=992283, PRELIM_GROSS_TOO_LOW=211912, OVER_CANDIDATE_CAP=125769, NO_POSITIVE_MARGINAL_EDGE=37784
- strike_inconsistency: NO_QUOTE=185306461, LOW_VOLUME=52549047, PRELIM_GROSS_TOO_LOW=8242507, LEG_NOT_TRADABLE=3347312, GROUPING_MISMATCH=82448
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
