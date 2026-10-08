# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 65 (65) | 49 (49) | 49 (49) | 45 |
| Oportunidades | 7333 | 7336 | 7262 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7333 | 690272 | 48103708 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.294 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05422 | 0.0463 | 0.02241 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 112.8 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7333
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=420774, LOW_VOLUME=194833, PRELIM_GROSS_TOO_LOW=38659, OVER_CANDIDATE_CAP=21693, NO_POSITIVE_MARGINAL_EDGE=7347
- strike_inconsistency: NO_QUOTE=36623674, LOW_VOLUME=9382451, PRELIM_GROSS_TOO_LOW=1472429, LEG_NOT_TRADABLE=587253, GROUPING_MISMATCH=16080
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
