# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 585 (585) | 569 (569) | 569 (569) | 45 |
| Oportunidades | 95208 | 85155 | 83779 | 0 |
| Net-positive | 2 | 0 | 2 | 0 |
| Ejecutables | 2 | 0 | 1 | 0 |
| Descartadas | 95206 | 8300287 | 562918289 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.995 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05543 | 0.04308 | 0.02121 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1.33 | n/d |
| Oport. por ciclo | 162.7 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 99.05 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0.952 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.02 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.002 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=95137, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5147707, LOW_VOLUME=2235682, PRELIM_GROSS_TOO_LOW=467081, OVER_CANDIDATE_CAP=282261, NO_POSITIVE_MARGINAL_EDGE=85314
- strike_inconsistency: NO_QUOTE=414917418, LOW_VOLUME=122177215, PRELIM_GROSS_TOO_LOW=18278323, LEG_NOT_TRADABLE=7060871, OVER_CANDIDATE_CAP=212534
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
