# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 366 (366) | 350 (350) | 350 (350) | 45 |
| Oportunidades | 60629 | 52386 | 51411 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 60627 | 5031776 | 343425922 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.045 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05604 | 0.04352 | 0.02162 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.7 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60580, SUSPICIOUS_EDGE_CHECK_RULES=47
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3142171, LOW_VOLUME=1331918, PRELIM_GROSS_TOO_LOW=283308, OVER_CANDIDATE_CAP=167276, NO_POSITIVE_MARGINAL_EDGE=52473
- strike_inconsistency: NO_QUOTE=258533565, LOW_VOLUME=69682446, PRELIM_GROSS_TOO_LOW=10538605, LEG_NOT_TRADABLE=4398051, GROUPING_MISMATCH=114141
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
