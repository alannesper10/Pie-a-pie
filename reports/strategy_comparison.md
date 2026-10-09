# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 86 (86) | 70 (70) | 70 (70) | 45 |
| Oportunidades | 10351 | 10481 | 10372 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10351 | 1009215 | 67244539 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.198 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05409 | 0.04549 | 0.02198 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 120.4 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10351
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=620111, LOW_VOLUME=281232, PRELIM_GROSS_TOO_LOW=55241, OVER_CANDIDATE_CAP=32066, NO_POSITIVE_MARGINAL_EDGE=10496
- strike_inconsistency: NO_QUOTE=50378743, LOW_VOLUME=13680021, PRELIM_GROSS_TOO_LOW=2151086, LEG_NOT_TRADABLE=978268, GROUPING_MISMATCH=23060
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
