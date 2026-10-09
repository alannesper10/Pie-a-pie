# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 95 (95) | 79 (79) | 79 (79) | 45 |
| Oportunidades | 11750 | 11830 | 11679 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 11750 | 1147922 | 76649903 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.189 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05406 | 0.04538 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.7 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=11750
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=705968, LOW_VOLUME=319388, PRELIM_GROSS_TOO_LOW=62271, OVER_CANDIDATE_CAP=36675, NO_POSITIVE_MARGINAL_EDGE=11846
- strike_inconsistency: NO_QUOTE=57540472, LOW_VOLUME=15597059, PRELIM_GROSS_TOO_LOW=2407682, LEG_NOT_TRADABLE=1040457, OVER_CANDIDATE_CAP=26179
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
