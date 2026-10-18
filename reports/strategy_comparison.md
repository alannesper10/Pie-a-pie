# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 570 (570) | 554 (554) | 554 (554) | 45 |
| Oportunidades | 92662 | 82909 | 81553 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 92660 | 8084041 | 547554985 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.996 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05547 | 0.04309 | 0.02121 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.6 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=92591, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5014546, LOW_VOLUME=2175298, PRELIM_GROSS_TOO_LOW=455469, OVER_CANDIDATE_CAP=275475, NO_POSITIVE_MARGINAL_EDGE=83064
- strike_inconsistency: NO_QUOTE=403613400, LOW_VOLUME=118729069, PRELIM_GROSS_TOO_LOW=17828050, LEG_NOT_TRADABLE=6912868, OVER_CANDIDATE_CAP=206828
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
