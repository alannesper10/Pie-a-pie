# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 20 (20) | 4 (4) | 4 (4) | 45 |
| Oportunidades | 2464 | 597 | 596 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2464 | 54934 | 4368919 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.578 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.0492 | 0.02149 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.2 | 149.2 | 149 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2464
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=33779, LOW_VOLUME=15217, PRELIM_GROSS_TOO_LOW=2937, OVER_CANDIDATE_CAP=1863, NO_POSITIVE_MARGINAL_EDGE=600
- strike_inconsistency: NO_QUOTE=3393555, LOW_VOLUME=824465, PRELIM_GROSS_TOO_LOW=124094, LEG_NOT_TRADABLE=23496, OVER_CANDIDATE_CAP=1369
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
