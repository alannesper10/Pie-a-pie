# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 122 (122) | 106 (106) | 106 (106) | 45 |
| Oportunidades | 16859 | 15868 | 15689 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 16859 | 1564734 | 104320183 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.184 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05422 | 0.04525 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 138.2 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=16859
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=966166, LOW_VOLUME=430901, PRELIM_GROSS_TOO_LOW=84756, OVER_CANDIDATE_CAP=51417, NO_POSITIVE_MARGINAL_EDGE=15893
- strike_inconsistency: NO_QUOTE=78560886, LOW_VOLUME=20969997, PRELIM_GROSS_TOO_LOW=3229715, LEG_NOT_TRADABLE=1475004, GROUPING_MISMATCH=34821
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
