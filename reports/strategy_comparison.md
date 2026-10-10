# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 204 (204) | 188 (188) | 188 (188) | 45 |
| Oportunidades | 34848 | 28139 | 27712 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 34848 | 2867167 | 185499229 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.138 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.04467 | 0.02215 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.8 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=34848
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1792075, LOW_VOLUME=761983, PRELIM_GROSS_TOO_LOW=158333, OVER_CANDIDATE_CAP=97533, NO_POSITIVE_MARGINAL_EDGE=28189
- strike_inconsistency: NO_QUOTE=136649005, LOW_VOLUME=39512996, PRELIM_GROSS_TOO_LOW=6317272, LEG_NOT_TRADABLE=2865246, OVER_CANDIDATE_CAP=64586
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
