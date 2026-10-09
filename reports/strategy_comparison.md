# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 137 (137) | 121 (121) | 121 (121) | 45 |
| Oportunidades | 19823 | 18111 | 17883 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 19823 | 1802794 | 115665235 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.182 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0544 | 0.04532 | 0.02192 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 144.7 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=19823
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1117423, LOW_VOLUME=492345, PRELIM_GROSS_TOO_LOW=97924, OVER_CANDIDATE_CAP=59277, NO_POSITIVE_MARGINAL_EDGE=18141
- strike_inconsistency: NO_QUOTE=86053890, LOW_VOLUME=23934980, PRELIM_GROSS_TOO_LOW=3744079, LEG_NOT_TRADABLE=1835434, GROUPING_MISMATCH=39696
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
