# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 53 (53) | 37 (37) | 37 (37) | 45 |
| Oportunidades | 5853 | 5542 | 5488 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5853 | 518518 | 37461494 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.383 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05439 | 0.04723 | 0.02243 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 110.4 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5853
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=314726, LOW_VOLUME=147376, PRELIM_GROSS_TOO_LOW=29342, OVER_CANDIDATE_CAP=16045, NO_POSITIVE_MARGINAL_EDGE=5548
- strike_inconsistency: NO_QUOTE=28955503, LOW_VOLUME=7122717, PRELIM_GROSS_TOO_LOW=1090835, LEG_NOT_TRADABLE=263786, GROUPING_MISMATCH=12145
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
