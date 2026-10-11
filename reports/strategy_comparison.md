# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 245 (245) | 229 (229) | 229 (229) | 45 |
| Oportunidades | 42821 | 34268 | 33595 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 42821 | 3458612 | 226576316 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.119 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05516 | 0.04431 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 174.8 | 149.6 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=42821
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2165442, LOW_VOLUME=913653, PRELIM_GROSS_TOO_LOW=192754, OVER_CANDIDATE_CAP=115947, NO_POSITIVE_MARGINAL_EDGE=34334
- strike_inconsistency: NO_QUOTE=167637981, LOW_VOLUME=47953049, PRELIM_GROSS_TOO_LOW=7607823, LEG_NOT_TRADABLE=3190158, OVER_CANDIDATE_CAP=77433
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
