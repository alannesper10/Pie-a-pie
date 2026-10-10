# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 178 (178) | 162 (162) | 162 (162) | 45 |
| Oportunidades | 29208 | 24248 | 23914 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 29208 | 2459794 | 158209035 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.15 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.0449 | 0.02208 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 164.1 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=29208
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1531543, LOW_VOLUME=661353, PRELIM_GROSS_TOO_LOW=134665, OVER_CANDIDATE_CAP=83343, NO_POSITIVE_MARGINAL_EDGE=24290
- strike_inconsistency: NO_QUOTE=116866483, LOW_VOLUME=33675941, PRELIM_GROSS_TOO_LOW=5241241, LEG_NOT_TRADABLE=2293928, OVER_CANDIDATE_CAP=53797
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
