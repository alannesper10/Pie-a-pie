# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 133 (133) | 117 (117) | 117 (117) | 45 |
| Oportunidades | 19111 | 17512 | 17295 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 19111 | 1739271 | 111903927 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.175 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05435 | 0.04524 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 143.7 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=19111
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1077053, LOW_VOLUME=475866, PRELIM_GROSS_TOO_LOW=94469, OVER_CANDIDATE_CAP=57210, NO_POSITIVE_MARGINAL_EDGE=17541
- strike_inconsistency: NO_QUOTE=83416049, LOW_VOLUME=22978290, PRELIM_GROSS_TOO_LOW=3606144, LEG_NOT_TRADABLE=1809717, GROUPING_MISMATCH=38396
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
