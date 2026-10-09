# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 92 (92) | 76 (76) | 76 (76) | 45 |
| Oportunidades | 11252 | 11381 | 11236 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 11252 | 1101857 | 73544376 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.189 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05405 | 0.04539 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122.3 | 149.8 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=11252
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=677510, LOW_VOLUME=306714, PRELIM_GROSS_TOO_LOW=59912, OVER_CANDIDATE_CAP=35088, NO_POSITIVE_MARGINAL_EDGE=11396
- strike_inconsistency: NO_QUOTE=55172645, LOW_VOLUME=14966545, PRELIM_GROSS_TOO_LOW=2321617, LEG_NOT_TRADABLE=1021677, OVER_CANDIDATE_CAP=25269
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
