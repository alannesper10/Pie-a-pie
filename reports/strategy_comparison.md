# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 399 (399) | 383 (383) | 383 (383) | 45 |
| Oportunidades | 64612 | 57325 | 56323 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 64610 | 5479370 | 373746986 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.031 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05613 | 0.04336 | 0.02152 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.9 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=64541, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3413051, LOW_VOLUME=1458049, PRELIM_GROSS_TOO_LOW=308911, OVER_CANDIDATE_CAP=183457, NO_POSITIVE_MARGINAL_EDGE=57422
- strike_inconsistency: NO_QUOTE=281670000, LOW_VOLUME=75647314, PRELIM_GROSS_TOO_LOW=11403526, LEG_NOT_TRADABLE=4725522, GROUPING_MISMATCH=124949
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
