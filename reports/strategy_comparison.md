# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 153 (153) | 137 (137) | 137 (137) | 45 |
| Oportunidades | 23113 | 20508 | 20211 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 23113 | 2060076 | 132326004 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.168 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05462 | 0.04519 | 0.02186 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 151.1 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=23113
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1280296, LOW_VOLUME=558436, PRELIM_GROSS_TOO_LOW=112187, OVER_CANDIDATE_CAP=68343, NO_POSITIVE_MARGINAL_EDGE=20541
- strike_inconsistency: NO_QUOTE=98101888, LOW_VOLUME=27822068, PRELIM_GROSS_TOO_LOW=4351858, LEG_NOT_TRADABLE=1937895, OVER_CANDIDATE_CAP=46575
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
