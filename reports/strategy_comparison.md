# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 192 (192) | 176 (176) | 176 (176) | 45 |
| Oportunidades | 32475 | 26344 | 26000 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 32475 | 2682154 | 172897477 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.138 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.0447 | 0.02217 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 169.1 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=32475
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1673717, LOW_VOLUME=716471, PRELIM_GROSS_TOO_LOW=147399, OVER_CANDIDATE_CAP=91212, NO_POSITIVE_MARGINAL_EDGE=26389
- strike_inconsistency: NO_QUOTE=127478975, LOW_VOLUME=36886867, PRELIM_GROSS_TOO_LOW=5790646, LEG_NOT_TRADABLE=2598429, OVER_CANDIDATE_CAP=58237
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
