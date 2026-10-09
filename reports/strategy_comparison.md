# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 131 (131) | 115 (115) | 115 (115) | 45 |
| Oportunidades | 18744 | 17212 | 16999 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 18744 | 1707467 | 110751447 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.174 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05433 | 0.04521 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 143.1 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=18744
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1056861, LOW_VOLUME=467616, PRELIM_GROSS_TOO_LOW=92689, OVER_CANDIDATE_CAP=56227, NO_POSITIVE_MARGINAL_EDGE=17241
- strike_inconsistency: NO_QUOTE=82704922, LOW_VOLUME=22618648, PRELIM_GROSS_TOO_LOW=3538991, LEG_NOT_TRADABLE=1796715, GROUPING_MISMATCH=37746
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
