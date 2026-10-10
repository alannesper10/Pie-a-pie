# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 183 (183) | 167 (167) | 167 (167) | 45 |
| Oportunidades | 30397 | 24997 | 24660 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 30397 | 2539319 | 163436309 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.146 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04482 | 0.02211 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 166.1 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=30397
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1582165, LOW_VOLUME=681388, PRELIM_GROSS_TOO_LOW=139227, OVER_CANDIDATE_CAP=86119, NO_POSITIVE_MARGINAL_EDGE=25039
- strike_inconsistency: NO_QUOTE=120637872, LOW_VOLUME=34833062, PRELIM_GROSS_TOO_LOW=5427915, LEG_NOT_TRADABLE=2402161, OVER_CANDIDATE_CAP=55269
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
