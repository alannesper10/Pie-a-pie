# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 34 (34) | 18 (18) | 18 (18) | 45 |
| Oportunidades | 4119 | 2695 | 2662 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4119 | 252032 | 19321534 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.576 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05458 | 0.04937 | 0.02178 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 121.1 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4119
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=153275, LOW_VOLUME=71245, PRELIM_GROSS_TOO_LOW=13364, OVER_CANDIDATE_CAP=8624, NO_POSITIVE_MARGINAL_EDGE=2699
- strike_inconsistency: NO_QUOTE=14993632, LOW_VOLUME=3655454, PRELIM_GROSS_TOO_LOW=546595, LEG_NOT_TRADABLE=110500, OVER_CANDIDATE_CAP=6647
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
