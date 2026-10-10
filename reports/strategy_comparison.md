# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 207 (207) | 191 (191) | 191 (191) | 45 |
| Oportunidades | 35415 | 28588 | 28114 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 35415 | 2912840 | 188473234 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05492 | 0.04466 | 0.02213 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.1 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=35415
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1821247, LOW_VOLUME=773369, PRELIM_GROSS_TOO_LOW=160998, OVER_CANDIDATE_CAP=98947, NO_POSITIVE_MARGINAL_EDGE=28639
- strike_inconsistency: NO_QUOTE=138804450, LOW_VOLUME=40152938, PRELIM_GROSS_TOO_LOW=6441849, LEG_NOT_TRADABLE=2916712, OVER_CANDIDATE_CAP=65709
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
