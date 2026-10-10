# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 162 (162) | 146 (146) | 146 (146) | 45 |
| Oportunidades | 25240 | 21855 | 21526 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 25240 | 2204822 | 141603153 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.158 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05475 | 0.04508 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 155.8 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=25240
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1371006, LOW_VOLUME=595949, PRELIM_GROSS_TOO_LOW=120186, OVER_CANDIDATE_CAP=73754, NO_POSITIVE_MARGINAL_EDGE=21891
- strike_inconsistency: NO_QUOTE=104862058, LOW_VOLUME=29956342, PRELIM_GROSS_TOO_LOW=4669652, LEG_NOT_TRADABLE=1995707, OVER_CANDIDATE_CAP=49381
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
