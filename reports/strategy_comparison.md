# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 147 (147) | 131 (131) | 131 (131) | 45 |
| Oportunidades | 21820 | 19609 | 19353 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 21820 | 1962497 | 126072948 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.176 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05453 | 0.04528 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 148.4 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=21820
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1219040, LOW_VOLUME=533044, PRELIM_GROSS_TOO_LOW=106832, OVER_CANDIDATE_CAP=64862, NO_POSITIVE_MARGINAL_EDGE=19641
- strike_inconsistency: NO_QUOTE=93573291, LOW_VOLUME=26371602, PRELIM_GROSS_TOO_LOW=4122252, LEG_NOT_TRADABLE=1899243, OVER_CANDIDATE_CAP=43702
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
