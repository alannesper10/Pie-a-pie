# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 168 (168) | 152 (152) | 152 (152) | 45 |
| Oportunidades | 26731 | 22754 | 22419 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 26731 | 2300801 | 147796782 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.156 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05482 | 0.04504 | 0.02199 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 159.1 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=26731
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1431206, LOW_VOLUME=620770, PRELIM_GROSS_TOO_LOW=125620, OVER_CANDIDATE_CAP=77374, NO_POSITIVE_MARGINAL_EDGE=22791
- strike_inconsistency: NO_QUOTE=109355450, LOW_VOLUME=31358606, PRELIM_GROSS_TOO_LOW=4880595, LEG_NOT_TRADABLE=2078348, OVER_CANDIDATE_CAP=50908
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
