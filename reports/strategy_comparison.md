# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 317 (317) | 301 (301) | 301 (301) | 45 |
| Oportunidades | 54314 | 45050 | 44121 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 54314 | 4390893 | 298052393 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.067 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0556 | 0.04371 | 0.02183 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.3 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=54314
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2752620, LOW_VOLUME=1152974, PRELIM_GROSS_TOO_LOW=247314, OVER_CANDIDATE_CAP=144831, NO_POSITIVE_MARGINAL_EDGE=45126
- strike_inconsistency: NO_QUOTE=223606068, LOW_VOLUME=61157614, PRELIM_GROSS_TOO_LOW=9331553, LEG_NOT_TRADABLE=3719781, GROUPING_MISMATCH=97962
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
