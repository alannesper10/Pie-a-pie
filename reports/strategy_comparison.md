# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 73 (73) | 57 (57) | 57 (57) | 45 |
| Oportunidades | 8405 | 8534 | 8446 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8405 | 810206 | 53652234 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.27 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05423 | 0.04611 | 0.02223 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 115.1 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8405
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=495598, LOW_VOLUME=227571, PRELIM_GROSS_TOO_LOW=44908, OVER_CANDIDATE_CAP=25576, NO_POSITIVE_MARGINAL_EDGE=8547
- strike_inconsistency: NO_QUOTE=40077686, LOW_VOLUME=10916771, PRELIM_GROSS_TOO_LOW=1719567, LEG_NOT_TRADABLE=893537, GROUPING_MISMATCH=18736
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
