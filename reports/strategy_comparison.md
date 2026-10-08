# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 69 (69) | 53 (53) | 53 (53) | 45 |
| Oportunidades | 7857 | 7934 | 7853 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7857 | 749958 | 50720375 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.286 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.0542 | 0.04624 | 0.02229 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 113.9 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7857
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=457914, LOW_VOLUME=211162, PRELIM_GROSS_TOO_LOW=41829, OVER_CANDIDATE_CAP=23628, NO_POSITIVE_MARGINAL_EDGE=7947
- strike_inconsistency: NO_QUOTE=38091624, LOW_VOLUME=10122246, PRELIM_GROSS_TOO_LOW=1597180, LEG_NOT_TRADABLE=867992, GROUPING_MISMATCH=17408
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
