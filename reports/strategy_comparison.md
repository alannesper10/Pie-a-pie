# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 177 (177) | 161 (161) | 161 (161) | 45 |
| Oportunidades | 28971 | 24099 | 23764 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 28971 | 2443897 | 157167269 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.151 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04492 | 0.02208 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 163.7 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=28971
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1521459, LOW_VOLUME=657323, PRELIM_GROSS_TOO_LOW=133745, OVER_CANDIDATE_CAP=82790, NO_POSITIVE_MARGINAL_EDGE=24140
- strike_inconsistency: NO_QUOTE=116114290, LOW_VOLUME=33445384, PRELIM_GROSS_TOO_LOW=5204547, LEG_NOT_TRADABLE=2272379, OVER_CANDIDATE_CAP=53501
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
