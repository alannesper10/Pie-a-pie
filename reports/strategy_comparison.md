# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 407 (407) | 391 (391) | 391 (391) | 45 |
| Oportunidades | 65608 | 58523 | 57499 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 65606 | 5592469 | 382138993 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.028 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.0561 | 0.04332 | 0.0215 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.2 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=65537, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3479542, LOW_VOLUME=1491646, PRELIM_GROSS_TOO_LOW=315644, OVER_CANDIDATE_CAP=187570, NO_POSITIVE_MARGINAL_EDGE=58621
- strike_inconsistency: NO_QUOTE=287698475, LOW_VOLUME=77367620, PRELIM_GROSS_TOO_LOW=11638437, LEG_NOT_TRADABLE=5127410, GROUPING_MISMATCH=127469
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
