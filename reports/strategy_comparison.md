# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 116 (116) | 100 (100) | 100 (100) | 45 |
| Oportunidades | 15623 | 14974 | 14804 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 15623 | 1470683 | 98668720 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.188 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05413 | 0.04528 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 134.7 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=15623
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=906637, LOW_VOLUME=406406, PRELIM_GROSS_TOO_LOW=79612, OVER_CANDIDATE_CAP=48195, NO_POSITIVE_MARGINAL_EDGE=14995
- strike_inconsistency: NO_QUOTE=74535331, LOW_VOLUME=19844075, PRELIM_GROSS_TOO_LOW=3035503, LEG_NOT_TRADABLE=1173996, GROUPING_MISMATCH=32871
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
