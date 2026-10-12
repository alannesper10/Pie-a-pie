# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 333 (333) | 317 (317) | 317 (317) | 45 |
| Oportunidades | 56682 | 47447 | 46509 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56682 | 4592875 | 310525655 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.055 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05565 | 0.04361 | 0.02175 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.2 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56678, SUSPICIOUS_EDGE_CHECK_RULES=4
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2878183, LOW_VOLUME=1206377, PRELIM_GROSS_TOO_LOW=259104, OVER_CANDIDATE_CAP=151529, NO_POSITIVE_MARGINAL_EDGE=47526
- strike_inconsistency: NO_QUOTE=233035436, LOW_VOLUME=63684939, PRELIM_GROSS_TOO_LOW=9719963, LEG_NOT_TRADABLE=3836987, GROUPING_MISMATCH=103113
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
