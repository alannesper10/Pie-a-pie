# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 115 (115) | 99 (99) | 99 (99) | 45 |
| Oportunidades | 15426 | 14825 | 14657 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 15426 | 1455116 | 97608148 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.188 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05413 | 0.04527 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 134.1 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=15426
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=896813, LOW_VOLUME=402312, PRELIM_GROSS_TOO_LOW=78785, OVER_CANDIDATE_CAP=47658, NO_POSITIVE_MARGINAL_EDGE=14845
- strike_inconsistency: NO_QUOTE=73706568, LOW_VOLUME=19651501, PRELIM_GROSS_TOO_LOW=3003393, LEG_NOT_TRADABLE=1167644, GROUPING_MISMATCH=32546
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
