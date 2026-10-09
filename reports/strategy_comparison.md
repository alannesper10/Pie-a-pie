# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 88 (88) | 72 (72) | 72 (72) | 45 |
| Oportunidades | 10648 | 10781 | 10651 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10648 | 1040225 | 69350968 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.195 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05406 | 0.04545 | 0.02195 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 121 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10648
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=639347, LOW_VOLUME=289772, PRELIM_GROSS_TOO_LOW=56804, OVER_CANDIDATE_CAP=33055, NO_POSITIVE_MARGINAL_EDGE=10796
- strike_inconsistency: NO_QUOTE=51977410, LOW_VOLUME=14111698, PRELIM_GROSS_TOO_LOW=2210258, LEG_NOT_TRADABLE=993156, OVER_CANDIDATE_CAP=23766
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
