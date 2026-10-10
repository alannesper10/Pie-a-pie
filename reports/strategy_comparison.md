# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 208 (208) | 192 (192) | 192 (192) | 45 |
| Oportunidades | 35604 | 28738 | 28253 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 35604 | 2927938 | 189361665 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05492 | 0.04466 | 0.02213 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.2 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=35604
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1830895, LOW_VOLUME=777143, PRELIM_GROSS_TOO_LOW=161870, OVER_CANDIDATE_CAP=99416, NO_POSITIVE_MARGINAL_EDGE=28789
- strike_inconsistency: NO_QUOTE=139424328, LOW_VOLUME=40371940, PRELIM_GROSS_TOO_LOW=6483459, LEG_NOT_TRADABLE=2923693, OVER_CANDIDATE_CAP=66185
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
