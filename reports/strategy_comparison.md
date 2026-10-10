# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 181 (181) | 165 (165) | 165 (165) | 45 |
| Oportunidades | 29913 | 24697 | 24361 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 29913 | 2507395 | 161334662 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.147 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05493 | 0.04485 | 0.02211 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 165.3 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=29913
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1561771, LOW_VOLUME=673405, PRELIM_GROSS_TOO_LOW=137431, OVER_CANDIDATE_CAP=84984, NO_POSITIVE_MARGINAL_EDGE=24739
- strike_inconsistency: NO_QUOTE=119123206, LOW_VOLUME=34366502, PRELIM_GROSS_TOO_LOW=5352499, LEG_NOT_TRADABLE=2358733, OVER_CANDIDATE_CAP=54646
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
