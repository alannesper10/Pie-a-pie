# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 156 (156) | 140 (140) | 140 (140) | 45 |
| Oportunidades | 23778 | 20958 | 20635 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 23778 | 2108523 | 135445393 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.165 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05466 | 0.04517 | 0.02184 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 152.4 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=23778
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1310708, LOW_VOLUME=570986, PRELIM_GROSS_TOO_LOW=114823, OVER_CANDIDATE_CAP=70132, NO_POSITIVE_MARGINAL_EDGE=20991
- strike_inconsistency: NO_QUOTE=100369612, LOW_VOLUME=28540100, PRELIM_GROSS_TOO_LOW=4463539, LEG_NOT_TRADABLE=1957304, OVER_CANDIDATE_CAP=47687
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
