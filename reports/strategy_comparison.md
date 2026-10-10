# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 170 (170) | 154 (154) | 154 (154) | 45 |
| Oportunidades | 27228 | 23054 | 22718 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 27228 | 2332692 | 149878977 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.155 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05484 | 0.04502 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 160.2 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=27228
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1451268, LOW_VOLUME=628959, PRELIM_GROSS_TOO_LOW=127447, OVER_CANDIDATE_CAP=78578, NO_POSITIVE_MARGINAL_EDGE=23091
- strike_inconsistency: NO_QUOTE=110856335, LOW_VOLUME=31823979, PRELIM_GROSS_TOO_LOW=4951926, LEG_NOT_TRADABLE=2121446, OVER_CANDIDATE_CAP=51462
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
