# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 42 (42) | 26 (26) | 26 (26) | 45 |
| Oportunidades | 4694 | 3894 | 3851 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4694 | 364537 | 26267711 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.543 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04892 | 0.02197 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 111.8 | 149.8 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4694
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=220979, LOW_VOLUME=103733, PRELIM_GROSS_TOO_LOW=20417, OVER_CANDIDATE_CAP=11496, NO_POSITIVE_MARGINAL_EDGE=3898
- strike_inconsistency: NO_QUOTE=20298518, LOW_VOLUME=5024915, PRELIM_GROSS_TOO_LOW=769305, LEG_NOT_TRADABLE=154497, GROUPING_MISMATCH=8570
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
