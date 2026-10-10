# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 160 (160) | 144 (144) | 144 (144) | 45 |
| Oportunidades | 24744 | 21557 | 21229 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 24744 | 2172753 | 139552220 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.16 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05472 | 0.04511 | 0.02186 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 154.7 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=24744
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1350908, LOW_VOLUME=587651, PRELIM_GROSS_TOO_LOW=118391, OVER_CANDIDATE_CAP=72534, NO_POSITIVE_MARGINAL_EDGE=21591
- strike_inconsistency: NO_QUOTE=103363839, LOW_VOLUME=29486229, PRELIM_GROSS_TOO_LOW=4601221, LEG_NOT_TRADABLE=1983017, OVER_CANDIDATE_CAP=48855
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
