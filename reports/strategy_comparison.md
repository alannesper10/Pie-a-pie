# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 27 (27) | 11 (11) | 11 (11) | 45 |
| Oportunidades | 3314 | 1647 | 1627 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3314 | 153496 | 12050453 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.558 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05477 | 0.04902 | 0.02144 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122.7 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3314
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=93685, LOW_VOLUME=43154, PRELIM_GROSS_TOO_LOW=8122, OVER_CANDIDATE_CAP=5220, NO_POSITIVE_MARGINAL_EDGE=1650
- strike_inconsistency: NO_QUOTE=9384359, LOW_VOLUME=2252452, PRELIM_GROSS_TOO_LOW=340827, LEG_NOT_TRADABLE=63058, OVER_CANDIDATE_CAP=4422
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
