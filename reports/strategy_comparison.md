# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 17 (17) | 1 (1) | 1 (1) | 45 |
| Oportunidades | 2100 | 149 | 150 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2100 | 13723 | 1090740 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.573 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05532 | 0.04913 | 0.02133 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 0.13 | n/d |
| Oport. por ciclo | 123.5 | 149 | 150 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2100
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8449, LOW_VOLUME=3802, PRELIM_GROSS_TOO_LOW=729, OVER_CANDIDATE_CAP=460, NO_POSITIVE_MARGINAL_EDGE=150
- strike_inconsistency: NO_QUOTE=848904, LOW_VOLUME=204993, PRELIM_GROSS_TOO_LOW=30265, LEG_NOT_TRADABLE=5755, OVER_CANDIDATE_CAP=338
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
