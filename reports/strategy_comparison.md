# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 121 (121) | 105 (105) | 105 (105) | 45 |
| Oportunidades | 16638 | 15719 | 15540 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 16638 | 1549051 | 103418028 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.186 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0542 | 0.04528 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 137.5 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=16638
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=956221, LOW_VOLUME=426853, PRELIM_GROSS_TOO_LOW=83896, OVER_CANDIDATE_CAP=50871, NO_POSITIVE_MARGINAL_EDGE=15743
- strike_inconsistency: NO_QUOTE=78146858, LOW_VOLUME=20783566, PRELIM_GROSS_TOO_LOW=3197034, LEG_NOT_TRADABLE=1206821, GROUPING_MISMATCH=34496
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
