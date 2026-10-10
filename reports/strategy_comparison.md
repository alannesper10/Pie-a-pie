# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 215 (215) | 199 (199) | 199 (199) | 45 |
| Oportunidades | 36942 | 29783 | 29255 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 36942 | 3032157 | 196441288 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.14 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05495 | 0.04464 | 0.02208 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.8 | 149.7 | 147 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=36942
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1897356, LOW_VOLUME=803285, PRELIM_GROSS_TOO_LOW=167845, OVER_CANDIDATE_CAP=102627, NO_POSITIVE_MARGINAL_EDGE=29838
- strike_inconsistency: NO_QUOTE=144662545, LOW_VOLUME=41877240, PRELIM_GROSS_TOO_LOW=6758059, LEG_NOT_TRADABLE=2977594, OVER_CANDIDATE_CAP=70402
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
