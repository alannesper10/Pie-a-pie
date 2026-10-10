# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 199 (199) | 183 (183) | 183 (183) | 45 |
| Oportunidades | 33870 | 27392 | 27021 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 33870 | 2790611 | 180257814 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.135 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04465 | 0.02217 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.2 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=33870
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1743127, LOW_VOLUME=743098, PRELIM_GROSS_TOO_LOW=153901, OVER_CANDIDATE_CAP=94911, NO_POSITIVE_MARGINAL_EDGE=27439
- strike_inconsistency: NO_QUOTE=132819236, LOW_VOLUME=38437307, PRELIM_GROSS_TOO_LOW=6099633, LEG_NOT_TRADABLE=2752691, OVER_CANDIDATE_CAP=61243
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
