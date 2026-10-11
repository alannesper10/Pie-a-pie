# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 233 (233) | 217 (217) | 217 (217) | 45 |
| Oportunidades | 40260 | 32472 | 31813 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 40260 | 3291614 | 214626288 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.134 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05504 | 0.04451 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.8 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=40260
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2060681, LOW_VOLUME=870317, PRELIM_GROSS_TOO_LOW=182918, OVER_CANDIDATE_CAP=110455, NO_POSITIVE_MARGINAL_EDGE=32536
- strike_inconsistency: NO_QUOTE=158485984, LOW_VOLUME=45547001, PRELIM_GROSS_TOO_LOW=7304606, LEG_NOT_TRADABLE=3108614, OVER_CANDIDATE_CAP=75935
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
