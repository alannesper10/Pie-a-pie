# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 26 (26) | 10 (10) | 10 (10) | 45 |
| Oportunidades | 3195 | 1497 | 1482 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3195 | 139397 | 10952779 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.554 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05481 | 0.04894 | 0.02149 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122.9 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3195
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=85110, LOW_VOLUME=39186, PRELIM_GROSS_TOO_LOW=7388, OVER_CANDIDATE_CAP=4725, NO_POSITIVE_MARGINAL_EDGE=1500
- strike_inconsistency: NO_QUOTE=8525339, LOW_VOLUME=2050159, PRELIM_GROSS_TOO_LOW=311045, LEG_NOT_TRADABLE=57402, OVER_CANDIDATE_CAP=3984
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
