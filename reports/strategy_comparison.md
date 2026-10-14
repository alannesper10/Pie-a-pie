# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 406 (406) | 390 (390) | 390 (390) | 45 |
| Oportunidades | 65480 | 58373 | 57349 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 65478 | 5578410 | 381095402 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.029 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05611 | 0.04333 | 0.0215 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.3 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=65409, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3471297, LOW_VOLUME=1487459, PRELIM_GROSS_TOO_LOW=314801, OVER_CANDIDATE_CAP=187045, NO_POSITIVE_MARGINAL_EDGE=58471
- strike_inconsistency: NO_QUOTE=286906960, LOW_VOLUME=77152390, PRELIM_GROSS_TOO_LOW=11609466, LEG_NOT_TRADABLE=5120269, GROUPING_MISMATCH=127154
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
