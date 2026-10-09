# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 126 (126) | 110 (110) | 110 (110) | 45 |
| Oportunidades | 17721 | 16467 | 16252 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 17721 | 1628059 | 107447102 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.175 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05428 | 0.04519 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 140.6 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=17721
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1006434, LOW_VOLUME=447117, PRELIM_GROSS_TOO_LOW=88328, OVER_CANDIDATE_CAP=53552, NO_POSITIVE_MARGINAL_EDGE=16493
- strike_inconsistency: NO_QUOTE=80777658, LOW_VOLUME=21713199, PRELIM_GROSS_TOO_LOW=3367847, LEG_NOT_TRADABLE=1500305, GROUPING_MISMATCH=36121
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
