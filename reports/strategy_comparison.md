# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 136 (136) | 120 (120) | 120 (120) | 45 |
| Oportunidades | 19642 | 17962 | 17733 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 19642 | 1786923 | 114626607 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.181 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05438 | 0.0453 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 144.4 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=19642
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1107323, LOW_VOLUME=488256, PRELIM_GROSS_TOO_LOW=97058, OVER_CANDIDATE_CAP=58747, NO_POSITIVE_MARGINAL_EDGE=17991
- strike_inconsistency: NO_QUOTE=85298578, LOW_VOLUME=23694184, PRELIM_GROSS_TOO_LOW=3708907, LEG_NOT_TRADABLE=1828896, GROUPING_MISMATCH=39371
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
