# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 265 (265) | 249 (249) | 249 (249) | 45 |
| Oportunidades | 47111 | 37265 | 36566 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 47111 | 3732484 | 246624964 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.1 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05537 | 0.0441 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.8 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=47111
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2339222, LOW_VOLUME=982371, PRELIM_GROSS_TOO_LOW=209414, OVER_CANDIDATE_CAP=124597, NO_POSITIVE_MARGINAL_EDGE=37334
- strike_inconsistency: NO_QUOTE=182984760, LOW_VOLUME=51962507, PRELIM_GROSS_TOO_LOW=8152380, LEG_NOT_TRADABLE=3325657, GROUPING_MISMATCH=81509
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
