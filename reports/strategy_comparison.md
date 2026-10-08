# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 25 (25) | 9 (9) | 9 (9) | 45 |
| Oportunidades | 3076 | 1347 | 1333 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3076 | 125292 | 9855547 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.554 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05487 | 0.0489 | 0.02154 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3076
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=76529, LOW_VOLUME=35210, PRELIM_GROSS_TOO_LOW=6637, OVER_CANDIDATE_CAP=4245, NO_POSITIVE_MARGINAL_EDGE=1350
- strike_inconsistency: NO_QUOTE=7669149, LOW_VOLUME=1846504, PRELIM_GROSS_TOO_LOW=280313, LEG_NOT_TRADABLE=51733, OVER_CANDIDATE_CAP=3483
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
