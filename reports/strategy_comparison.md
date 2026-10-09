# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 144 (144) | 128 (128) | 128 (128) | 45 |
| Oportunidades | 21213 | 19159 | 18911 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 21213 | 1914259 | 122946841 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.178 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04529 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 147.3 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=21213
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1188428, LOW_VOLUME=520749, PRELIM_GROSS_TOO_LOW=104138, OVER_CANDIDATE_CAP=63136, NO_POSITIVE_MARGINAL_EDGE=19191
- strike_inconsistency: NO_QUOTE=91318614, LOW_VOLUME=25638939, PRELIM_GROSS_TOO_LOW=4005557, LEG_NOT_TRADABLE=1880211, OVER_CANDIDATE_CAP=42093
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
