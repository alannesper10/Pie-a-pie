# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 39 (39) | 23 (23) | 23 (23) | 45 |
| Oportunidades | 4616 | 3444 | 3401 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4616 | 322443 | 23689931 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.576 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04932 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 118.4 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4616
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=195645, LOW_VOLUME=91566, PRELIM_GROSS_TOO_LOW=17372, OVER_CANDIDATE_CAP=10901, NO_POSITIVE_MARGINAL_EDGE=3448
- strike_inconsistency: NO_QUOTE=18232293, LOW_VOLUME=4608467, PRELIM_GROSS_TOO_LOW=692295, LEG_NOT_TRADABLE=138051, OVER_CANDIDATE_CAP=7734
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
