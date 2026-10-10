# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 148 (148) | 132 (132) | 132 (132) | 45 |
| Oportunidades | 22032 | 19759 | 19500 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 22032 | 1978788 | 127115425 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.175 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05455 | 0.04527 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 148.9 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=22032
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1229281, LOW_VOLUME=537281, PRELIM_GROSS_TOO_LOW=107743, OVER_CANDIDATE_CAP=65440, NO_POSITIVE_MARGINAL_EDGE=19791
- strike_inconsistency: NO_QUOTE=94325671, LOW_VOLUME=26615038, PRELIM_GROSS_TOO_LOW=4161530, LEG_NOT_TRADABLE=1905620, OVER_CANDIDATE_CAP=44231
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
