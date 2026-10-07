# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 19 (19) | 3 (3) | 3 (3) | 45 |
| Oportunidades | 2343 | 448 | 447 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2343 | 41197 | 3276024 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.552 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05526 | 0.04888 | 0.02154 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.3 | 149.3 | 149 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2343
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=25338, LOW_VOLUME=11417, PRELIM_GROSS_TOO_LOW=2198, OVER_CANDIDATE_CAP=1396, NO_POSITIVE_MARGINAL_EDGE=450
- strike_inconsistency: NO_QUOTE=2544688, LOW_VOLUME=618203, PRELIM_GROSS_TOO_LOW=92768, LEG_NOT_TRADABLE=17880, OVER_CANDIDATE_CAP=1030
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
