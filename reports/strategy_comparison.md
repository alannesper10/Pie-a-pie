# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 296 (296) | 280 (280) | 280 (280) | 45 |
| Oportunidades | 51389 | 41906 | 41002 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 51389 | 4129783 | 277216322 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.075 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05554 | 0.0438 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 173.6 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=51389
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2590644, LOW_VOLUME=1083632, PRELIM_GROSS_TOO_LOW=232645, OVER_CANDIDATE_CAP=136025, NO_POSITIVE_MARGINAL_EDGE=41977
- strike_inconsistency: NO_QUOTE=206909581, LOW_VOLUME=57604815, PRELIM_GROSS_TOO_LOW=8905350, LEG_NOT_TRADABLE=3572800, GROUPING_MISMATCH=91473
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
