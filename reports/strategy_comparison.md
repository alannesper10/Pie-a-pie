# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 187 (187) | 171 (171) | 171 (171) | 45 |
| Oportunidades | 31338 | 25596 | 25256 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 31338 | 2603070 | 167640888 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.142 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04477 | 0.02212 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 167.6 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=31338
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1623034, LOW_VOLUME=697174, PRELIM_GROSS_TOO_LOW=142774, OVER_CANDIDATE_CAP=88400, NO_POSITIVE_MARGINAL_EDGE=25639
- strike_inconsistency: NO_QUOTE=123672616, LOW_VOLUME=35756497, PRELIM_GROSS_TOO_LOW=5583922, LEG_NOT_TRADABLE=2489395, OVER_CANDIDATE_CAP=56520
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
