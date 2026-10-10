# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 198 (198) | 182 (182) | 182 (182) | 45 |
| Oportunidades | 33667 | 27242 | 26877 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 33667 | 2775182 | 179207676 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.135 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04465 | 0.02218 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=33667
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1733264, LOW_VOLUME=739319, PRELIM_GROSS_TOO_LOW=152974, OVER_CANDIDATE_CAP=94384, NO_POSITIVE_MARGINAL_EDGE=27289
- strike_inconsistency: NO_QUOTE=132055292, LOW_VOLUME=38219255, PRELIM_GROSS_TOO_LOW=6055004, LEG_NOT_TRADABLE=2730257, OVER_CANDIDATE_CAP=60648
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
