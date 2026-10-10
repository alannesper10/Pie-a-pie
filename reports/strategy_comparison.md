# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 164 (164) | 148 (148) | 148 (148) | 45 |
| Oportunidades | 25738 | 22155 | 21825 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 25738 | 2236879 | 143652853 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.157 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05477 | 0.04506 | 0.02193 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 156.9 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=25738
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1391098, LOW_VOLUME=604272, PRELIM_GROSS_TOO_LOW=121982, OVER_CANDIDATE_CAP=74963, NO_POSITIVE_MARGINAL_EDGE=22191
- strike_inconsistency: NO_QUOTE=106359463, LOW_VOLUME=30424950, PRELIM_GROSS_TOO_LOW=4739261, LEG_NOT_TRADABLE=2008322, OVER_CANDIDATE_CAP=49890
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
