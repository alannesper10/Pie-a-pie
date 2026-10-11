# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 256 (256) | 240 (240) | 240 (240) | 45 |
| Oportunidades | 45282 | 35916 | 35233 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 45282 | 3610555 | 237575819 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.108 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05528 | 0.04418 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 176.9 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=45282
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2261549, LOW_VOLUME=952128, PRELIM_GROSS_TOO_LOW=202069, OVER_CANDIDATE_CAP=120773, NO_POSITIVE_MARGINAL_EDGE=35984
- strike_inconsistency: NO_QUOTE=176041800, LOW_VOLUME=50177464, PRELIM_GROSS_TOO_LOW=7898821, LEG_NOT_TRADABLE=3263810, OVER_CANDIDATE_CAP=78807
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
