# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 140 (140) | 124 (124) | 124 (124) | 45 |
| Oportunidades | 20409 | 18560 | 18330 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 20409 | 1850441 | 118782156 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.182 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05443 | 0.04533 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 145.8 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=20409
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1147752, LOW_VOLUME=504556, PRELIM_GROSS_TOO_LOW=100554, OVER_CANDIDATE_CAP=60907, NO_POSITIVE_MARGINAL_EDGE=18591
- strike_inconsistency: NO_QUOTE=88318250, LOW_VOLUME=24657918, PRELIM_GROSS_TOO_LOW=3851961, LEG_NOT_TRADABLE=1854656, GROUPING_MISMATCH=40671
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
