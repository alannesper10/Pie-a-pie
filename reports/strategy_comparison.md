# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 742 (742) | 726 (725) | 726 (725) | 45 |
| Oportunidades | 114848 | 108505 | 106743 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 114846 | 10480186 | 718697183 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.969 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05519 | 0.04263 | 0.02116 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.8 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=114777, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6466730, LOW_VOLUME=2852939, PRELIM_GROSS_TOO_LOW=591923, OVER_CANDIDATE_CAP=357720, NO_POSITIVE_MARGINAL_EDGE=108708
- strike_inconsistency: NO_QUOTE=527575522, LOW_VOLUME=157904728, PRELIM_GROSS_TOO_LOW=23433135, LEG_NOT_TRADABLE=9157893, OVER_CANDIDATE_CAP=280638
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
