# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 768 (768) | 752 (751) | 752 (751) | 45 |
| Oportunidades | 118362 | 112397 | 110596 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 118360 | 10887066 | 744753444 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.961 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05518 | 0.04251 | 0.02113 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.1 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=118291, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6714439, LOW_VOLUME=2965739, PRELIM_GROSS_TOO_LOW=616186, OVER_CANDIDATE_CAP=372262, NO_POSITIVE_MARGINAL_EDGE=112608
- strike_inconsistency: NO_QUOTE=545788153, LOW_VOLUME=164388162, PRELIM_GROSS_TOO_LOW=24427404, LEG_NOT_TRADABLE=9495299, OVER_CANDIDATE_CAP=296881
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
