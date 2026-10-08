# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 60 (60) | 44 (44) | 44 (44) | 45 |
| Oportunidades | 6688 | 6587 | 6523 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 6688 | 617874 | 44278694 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.326 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05428 | 0.04662 | 0.02249 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 111.5 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=6688
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=375964, LOW_VOLUME=174928, PRELIM_GROSS_TOO_LOW=34765, OVER_CANDIDATE_CAP=19279, NO_POSITIVE_MARGINAL_EDGE=6597
- strike_inconsistency: NO_QUOTE=33931304, LOW_VOLUME=8448272, PRELIM_GROSS_TOO_LOW=1307928, LEG_NOT_TRADABLE=557296, GROUPING_MISMATCH=14420
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
