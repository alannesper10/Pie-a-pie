# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 110 (110) | 94 (94) | 94 (94) | 45 |
| Oportunidades | 14458 | 14077 | 13914 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 14458 | 1378105 | 92327343 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.185 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05411 | 0.04523 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 131.4 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=14458
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=848624, LOW_VOLUME=381808, PRELIM_GROSS_TOO_LOW=74663, OVER_CANDIDATE_CAP=44927, NO_POSITIVE_MARGINAL_EDGE=14096
- strike_inconsistency: NO_QUOTE=69601668, LOW_VOLUME=18662448, PRELIM_GROSS_TOO_LOW=2851722, LEG_NOT_TRADABLE=1136195, GROUPING_MISMATCH=30921
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
