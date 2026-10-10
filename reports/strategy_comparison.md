# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 184 (184) | 168 (168) | 168 (168) | 45 |
| Oportunidades | 30639 | 25147 | 24809 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 30639 | 2555273 | 164487360 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.145 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04481 | 0.02211 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 166.5 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=30639
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1592388, LOW_VOLUME=685356, PRELIM_GROSS_TOO_LOW=140114, OVER_CANDIDATE_CAP=86688, NO_POSITIVE_MARGINAL_EDGE=25189
- strike_inconsistency: NO_QUOTE=121395666, LOW_VOLUME=35065543, PRELIM_GROSS_TOO_LOW=5466191, LEG_NOT_TRADABLE=2423889, OVER_CANDIDATE_CAP=55564
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
