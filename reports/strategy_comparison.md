# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 535 (535) | 519 (519) | 519 (519) | 45 |
| Oportunidades | 86009 | 77674 | 76462 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 86007 | 7533808 | 510418389 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.999 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05564 | 0.04309 | 0.02127 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 160.8 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=85938, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4667489, LOW_VOLUME=2030826, PRELIM_GROSS_TOO_LOW=425316, OVER_CANDIDATE_CAP=256768, NO_POSITIVE_MARGINAL_EDGE=77814
- strike_inconsistency: NO_QUOTE=378122931, LOW_VOLUME=109139146, PRELIM_GROSS_TOO_LOW=16150035, LEG_NOT_TRADABLE=6581496, OVER_CANDIDATE_CAP=177132
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
