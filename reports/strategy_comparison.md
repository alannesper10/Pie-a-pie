# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 38 (38) | 22 (22) | 22 (22) | 45 |
| Oportunidades | 4583 | 3294 | 3251 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4583 | 308408 | 22830671 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.581 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04937 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 120.6 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4583
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=187200, LOW_VOLUME=87515, PRELIM_GROSS_TOO_LOW=16402, OVER_CANDIDATE_CAP=10644, NO_POSITIVE_MARGINAL_EDGE=3298
- strike_inconsistency: NO_QUOTE=17555364, LOW_VOLUME=4459541, PRELIM_GROSS_TOO_LOW=664943, LEG_NOT_TRADABLE=132569, OVER_CANDIDATE_CAP=7640
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
