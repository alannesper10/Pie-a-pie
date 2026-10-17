# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 554 (554) | 538 (538) | 538 (538) | 45 |
| Oportunidades | 89974 | 80519 | 79303 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 89972 | 7839330 | 530904829 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.994 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05553 | 0.04306 | 0.02124 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.4 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=89903, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4860598, LOW_VOLUME=2110489, PRELIM_GROSS_TOO_LOW=442078, OVER_CANDIDATE_CAP=267829, NO_POSITIVE_MARGINAL_EDGE=80664
- strike_inconsistency: NO_QUOTE=391934774, LOW_VOLUME=114684905, PRELIM_GROSS_TOO_LOW=17085188, LEG_NOT_TRADABLE=6753735, OVER_CANDIDATE_CAP=189197
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
