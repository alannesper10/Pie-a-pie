# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 883 (883) | 867 (866) | 867 (866) | 45 |
| Oportunidades | 138958 | 129611 | 127506 | 0 |
| Net-positive | 2 | 0 | 44 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 138956 | 12825310 | 875362006 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.943 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0551 | 0.04226 | 0.02107 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 157.4 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=138887, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7851221, LOW_VOLUME=3548010, PRELIM_GROSS_TOO_LOW=726195, OVER_CANDIDATE_CAP=444869, NO_POSITIVE_MARGINAL_EDGE=129850
- strike_inconsistency: NO_QUOTE=635330165, LOW_VOLUME=198452044, PRELIM_GROSS_TOO_LOW=28928727, LEG_NOT_TRADABLE=11885786, OVER_CANDIDATE_CAP=352310
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
