# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 171 (171) | 155 (155) | 155 (155) | 45 |
| Oportunidades | 27478 | 23202 | 22868 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 27478 | 2348618 | 150920074 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.155 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05485 | 0.04501 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 160.7 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=27478
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1461293, LOW_VOLUME=633040, PRELIM_GROSS_TOO_LOW=128348, OVER_CANDIDATE_CAP=79190, NO_POSITIVE_MARGINAL_EDGE=23241
- strike_inconsistency: NO_QUOTE=111606901, LOW_VOLUME=32056332, PRELIM_GROSS_TOO_LOW=4987777, LEG_NOT_TRADABLE=2142995, OVER_CANDIDATE_CAP=51763
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
