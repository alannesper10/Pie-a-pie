# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 158 (158) | 142 (142) | 142 (142) | 45 |
| Oportunidades | 24249 | 21257 | 20933 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 24249 | 2140670 | 137500484 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.162 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05469 | 0.04514 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 153.5 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=24249
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1330826, LOW_VOLUME=579326, PRELIM_GROSS_TOO_LOW=116609, OVER_CANDIDATE_CAP=71329, NO_POSITIVE_MARGINAL_EDGE=21291
- strike_inconsistency: NO_QUOTE=101867836, LOW_VOLUME=29012992, PRELIM_GROSS_TOO_LOW=4532961, LEG_NOT_TRADABLE=1970277, OVER_CANDIDATE_CAP=48313
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
