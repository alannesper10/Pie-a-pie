# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 174 (174) | 158 (158) | 158 (158) | 45 |
| Oportunidades | 28224 | 23651 | 23314 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 28224 | 2396355 | 154043636 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.154 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05488 | 0.04497 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 162.2 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=28224
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1491394, LOW_VOLUME=645234, PRELIM_GROSS_TOO_LOW=131034, OVER_CANDIDATE_CAP=81018, NO_POSITIVE_MARGINAL_EDGE=23691
- strike_inconsistency: NO_QUOTE=113859667, LOW_VOLUME=32752288, PRELIM_GROSS_TOO_LOW=5095621, LEG_NOT_TRADABLE=2207696, OVER_CANDIDATE_CAP=52627
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
