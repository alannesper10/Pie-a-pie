# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 185 (185) | 169 (169) | 169 (169) | 45 |
| Oportunidades | 30865 | 25297 | 24958 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 30865 | 2571208 | 165538452 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.144 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.0448 | 0.02212 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 166.8 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=30865
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1602601, LOW_VOLUME=689298, PRELIM_GROSS_TOO_LOW=141000, OVER_CANDIDATE_CAP=87258, NO_POSITIVE_MARGINAL_EDGE=25339
- strike_inconsistency: NO_QUOTE=122154781, LOW_VOLUME=35296043, PRELIM_GROSS_TOO_LOW=5505038, LEG_NOT_TRADABLE=2445724, OVER_CANDIDATE_CAP=55882
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
