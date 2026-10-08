# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 80 (80) | 64 (64) | 64 (64) | 45 |
| Oportunidades | 9445 | 9584 | 9489 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9445 | 916666 | 60933760 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.231 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05421 | 0.04576 | 0.02209 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 118.1 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9445
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=562366, LOW_VOLUME=256161, PRELIM_GROSS_TOO_LOW=50428, OVER_CANDIDATE_CAP=29082, NO_POSITIVE_MARGINAL_EDGE=9597
- strike_inconsistency: NO_QUOTE=45599753, LOW_VOLUME=12395025, PRELIM_GROSS_TOO_LOW=1949613, LEG_NOT_TRADABLE=938642, GROUPING_MISMATCH=21060
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
