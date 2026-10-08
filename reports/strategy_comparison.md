# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 49 (49) | 33 (33) | 33 (33) | 45 |
| Oportunidades | 5372 | 4944 | 4896 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5372 | 462512 | 33265424 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.432 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05445 | 0.04772 | 0.02224 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.6 | 149.8 | 148.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5372
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=280397, LOW_VOLUME=131708, PRELIM_GROSS_TOO_LOW=26260, OVER_CANDIDATE_CAP=14237, NO_POSITIVE_MARGINAL_EDGE=4948
- strike_inconsistency: NO_QUOTE=25688932, LOW_VOLUME=6340032, PRELIM_GROSS_TOO_LOW=969374, LEG_NOT_TRADABLE=241444, GROUPING_MISMATCH=10845
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
