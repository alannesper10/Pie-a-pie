# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 119 (119) | 103 (103) | 103 (103) | 45 |
| Oportunidades | 16216 | 15421 | 15249 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 16216 | 1517662 | 101615324 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.189 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05417 | 0.0453 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 136.3 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=16216
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=936315, LOW_VOLUME=418752, PRELIM_GROSS_TOO_LOW=82167, OVER_CANDIDATE_CAP=49768, NO_POSITIVE_MARGINAL_EDGE=15444
- strike_inconsistency: NO_QUOTE=76797427, LOW_VOLUME=20409880, PRELIM_GROSS_TOO_LOW=3131643, LEG_NOT_TRADABLE=1194250, GROUPING_MISMATCH=33846
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
