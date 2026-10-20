# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 681 (681) | 665 (665) | 665 (665) | 45 |
| Oportunidades | 107424 | 99526 | 97813 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 107422 | 9584313 | 658436339 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.986 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05525 | 0.04291 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 157.7 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=107353, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5931490, LOW_VOLUME=2592678, PRELIM_GROSS_TOO_LOW=539919, OVER_CANDIDATE_CAP=325694, NO_POSITIVE_MARGINAL_EDGE=99709
- strike_inconsistency: NO_QUOTE=485579947, LOW_VOLUME=142785862, PRELIM_GROSS_TOO_LOW=21111608, LEG_NOT_TRADABLE=8397427, OVER_CANDIDATE_CAP=244433
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
