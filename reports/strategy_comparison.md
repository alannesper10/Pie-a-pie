# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 173 (173) | 157 (157) | 157 (157) | 45 |
| Oportunidades | 27976 | 23501 | 23165 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 27976 | 2380469 | 153002472 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.154 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05487 | 0.04498 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 161.7 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=27976
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1481367, LOW_VOLUME=641182, PRELIM_GROSS_TOO_LOW=130138, OVER_CANDIDATE_CAP=80415, NO_POSITIVE_MARGINAL_EDGE=23541
- strike_inconsistency: NO_QUOTE=113108921, LOW_VOLUME=32520213, PRELIM_GROSS_TOO_LOW=5059609, LEG_NOT_TRADABLE=2186130, OVER_CANDIDATE_CAP=52339
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
