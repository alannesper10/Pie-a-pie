# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 159 (159) | 143 (143) | 143 (143) | 45 |
| Oportunidades | 24499 | 21407 | 21081 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 24499 | 2156719 | 138526356 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.161 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0547 | 0.04512 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 154.1 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=24499
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1340863, LOW_VOLUME=583493, PRELIM_GROSS_TOO_LOW=117494, OVER_CANDIDATE_CAP=71931, NO_POSITIVE_MARGINAL_EDGE=21441
- strike_inconsistency: NO_QUOTE=102615635, LOW_VOLUME=29249866, PRELIM_GROSS_TOO_LOW=4567042, LEG_NOT_TRADABLE=1976657, OVER_CANDIDATE_CAP=48574
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
