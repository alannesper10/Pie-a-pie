# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 301 (301) | 285 (285) | 285 (285) | 45 |
| Oportunidades | 52025 | 42656 | 41726 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52025 | 4192382 | 282197059 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.073 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05556 | 0.04377 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.8 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52025
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2629380, LOW_VOLUME=1100392, PRELIM_GROSS_TOO_LOW=236047, OVER_CANDIDATE_CAP=138089, NO_POSITIVE_MARGINAL_EDGE=42727
- strike_inconsistency: NO_QUOTE=210895763, LOW_VOLUME=58464819, PRELIM_GROSS_TOO_LOW=9000698, LEG_NOT_TRADABLE=3608708, GROUPING_MISMATCH=93018
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
