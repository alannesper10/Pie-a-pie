# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 206 (206) | 190 (190) | 190 (190) | 45 |
| Oportunidades | 35229 | 28439 | 27972 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 35229 | 2897668 | 187582246 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.04467 | 0.02214 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=35229
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1811551, LOW_VOLUME=769580, PRELIM_GROSS_TOO_LOW=160127, OVER_CANDIDATE_CAP=98472, NO_POSITIVE_MARGINAL_EDGE=28489
- strike_inconsistency: NO_QUOTE=138183994, LOW_VOLUME=39931713, PRELIM_GROSS_TOO_LOW=6400283, LEG_NOT_TRADABLE=2909777, OVER_CANDIDATE_CAP=65387
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
