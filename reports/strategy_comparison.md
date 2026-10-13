# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 391 (391) | 375 (375) | 375 (375) | 45 |
| Oportunidades | 63704 | 56126 | 55128 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 63702 | 5369048 | 365428450 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.034 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05616 | 0.04338 | 0.02154 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.9 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=63633, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3346339, LOW_VOLUME=1426580, PRELIM_GROSS_TOO_LOW=302694, OVER_CANDIDATE_CAP=179640, NO_POSITIVE_MARGINAL_EDGE=56222
- strike_inconsistency: NO_QUOTE=275228264, LOW_VOLUME=74062298, PRELIM_GROSS_TOO_LOW=11174915, LEG_NOT_TRADABLE=4669204, GROUPING_MISMATCH=122429
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
