# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 31 (31) | 15 (15) | 15 (15) | 45 |
| Oportunidades | 3782 | 2246 | 2215 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3782 | 209750 | 16359813 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.578 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05466 | 0.04938 | 0.02155 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3782
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=127878, LOW_VOLUME=58998, PRELIM_GROSS_TOO_LOW=11099, OVER_CANDIDATE_CAP=7180, NO_POSITIVE_MARGINAL_EDGE=2250
- strike_inconsistency: NO_QUOTE=12739764, LOW_VOLUME=3053937, PRELIM_GROSS_TOO_LOW=459106, LEG_NOT_TRADABLE=93889, OVER_CANDIDATE_CAP=5842
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
