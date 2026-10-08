# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 52 (52) | 36 (36) | 36 (36) | 45 |
| Oportunidades | 5734 | 5392 | 5339 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5734 | 504489 | 36408635 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.396 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.0544 | 0.04737 | 0.02238 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 110.3 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5734
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=306097, LOW_VOLUME=143464, PRELIM_GROSS_TOO_LOW=28589, OVER_CANDIDATE_CAP=15589, NO_POSITIVE_MARGINAL_EDGE=5398
- strike_inconsistency: NO_QUOTE=28131582, LOW_VOLUME=6930675, PRELIM_GROSS_TOO_LOW=1060339, LEG_NOT_TRADABLE=258123, GROUPING_MISMATCH=11820
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
