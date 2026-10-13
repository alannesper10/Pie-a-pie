# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 367 (367) | 351 (351) | 351 (351) | 45 |
| Oportunidades | 60755 | 52536 | 51561 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 60753 | 5045228 | 344450415 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.045 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05605 | 0.04352 | 0.02162 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.5 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60705, SUSPICIOUS_EDGE_CHECK_RULES=48
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3150195, LOW_VOLUME=1335758, PRELIM_GROSS_TOO_LOW=284103, OVER_CANDIDATE_CAP=167808, NO_POSITIVE_MARGINAL_EDGE=52623
- strike_inconsistency: NO_QUOTE=259347522, LOW_VOLUME=69860643, PRELIM_GROSS_TOO_LOW=10563214, LEG_NOT_TRADABLE=4404994, GROUPING_MISMATCH=114472
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
