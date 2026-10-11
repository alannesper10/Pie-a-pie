# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 284 (284) | 268 (268) | 268 (268) | 45 |
| Oportunidades | 49917 | 40112 | 39259 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 49917 | 3979918 | 265262715 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.081 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05548 | 0.04387 | 0.02197 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 175.8 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=49917
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2496903, LOW_VOLUME=1044324, PRELIM_GROSS_TOO_LOW=224325, OVER_CANDIDATE_CAP=131519, NO_POSITIVE_MARGINAL_EDGE=40181
- strike_inconsistency: NO_QUOTE=197380797, LOW_VOLUME=55520652, PRELIM_GROSS_TOO_LOW=8665977, LEG_NOT_TRADABLE=3479984, GROUPING_MISMATCH=87688
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
