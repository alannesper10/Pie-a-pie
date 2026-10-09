# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 97 (97) | 81 (81) | 81 (81) | 45 |
| Oportunidades | 12097 | 12130 | 11975 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12097 | 1178644 | 78723120 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05407 | 0.04535 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 124.7 | 149.8 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12097
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=724995, LOW_VOLUME=327771, PRELIM_GROSS_TOO_LOW=63880, OVER_CANDIDATE_CAP=37744, NO_POSITIVE_MARGINAL_EDGE=12146
- strike_inconsistency: NO_QUOTE=59123534, LOW_VOLUME=16015131, PRELIM_GROSS_TOO_LOW=2465540, LEG_NOT_TRADABLE=1053179, OVER_CANDIDATE_CAP=26728
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
