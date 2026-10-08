# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 36 (36) | 20 (20) | 20 (20) | 45 |
| Oportunidades | 4352 | 2994 | 2960 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4352 | 280250 | 21086894 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.581 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05454 | 0.0494 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 120.9 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4352
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=170242, LOW_VOLUME=79399, PRELIM_GROSS_TOO_LOW=14871, OVER_CANDIDATE_CAP=9641, NO_POSITIVE_MARGINAL_EDGE=2998
- strike_inconsistency: NO_QUOTE=16286205, LOW_VOLUME=4057094, PRELIM_GROSS_TOO_LOW=605335, LEG_NOT_TRADABLE=121464, OVER_CANDIDATE_CAP=7136
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
