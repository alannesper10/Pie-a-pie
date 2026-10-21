# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 719 (719) | 703 (703) | 703 (703) | 45 |
| Oportunidades | 111914 | 105212 | 103464 | 0 |
| Net-positive | 2 | 0 | 37 | 0 |
| Ejecutables | 2 | 0 | 36 | 0 |
| Descartadas | 111912 | 10142440 | 696566279 | 2412 |
| Duración media (min) | 0 | n/d | 19.05 | n/d |
| Capital por paquete (media) | 1.014 | 1.977 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05521 | 0.04275 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.7 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=111843, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6264180, LOW_VOLUME=2756653, PRELIM_GROSS_TOO_LOW=571346, OVER_CANDIDATE_CAP=345740, NO_POSITIVE_MARGINAL_EDGE=105409
- strike_inconsistency: NO_QUOTE=512317494, LOW_VOLUME=152225439, PRELIM_GROSS_TOO_LOW=22549714, LEG_NOT_TRADABLE=8872342, OVER_CANDIDATE_CAP=266516
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
