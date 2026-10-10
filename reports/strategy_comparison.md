# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 209 (209) | 193 (193) | 193 (193) | 45 |
| Oportunidades | 35789 | 28887 | 28394 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 35789 | 2942964 | 190249373 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.14 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05492 | 0.04467 | 0.02212 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.2 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=35789
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1840488, LOW_VOLUME=780923, PRELIM_GROSS_TOO_LOW=162713, OVER_CANDIDATE_CAP=99887, NO_POSITIVE_MARGINAL_EDGE=28939
- strike_inconsistency: NO_QUOTE=140043445, LOW_VOLUME=40590690, PRELIM_GROSS_TOO_LOW=6524529, LEG_NOT_TRADABLE=2931477, OVER_CANDIDATE_CAP=66688
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
