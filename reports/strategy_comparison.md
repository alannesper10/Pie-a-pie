# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 161 (161) | 145 (145) | 145 (145) | 45 |
| Oportunidades | 24993 | 21707 | 21379 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 24993 | 2188790 | 140578106 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.159 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05473 | 0.0451 | 0.02187 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 155.2 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=24993
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1360962, LOW_VOLUME=591801, PRELIM_GROSS_TOO_LOW=119284, OVER_CANDIDATE_CAP=73142, NO_POSITIVE_MARGINAL_EDGE=21741
- strike_inconsistency: NO_QUOTE=104112655, LOW_VOLUME=29722032, PRELIM_GROSS_TOO_LOW=4635365, LEG_NOT_TRADABLE=1989403, OVER_CANDIDATE_CAP=49115
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
