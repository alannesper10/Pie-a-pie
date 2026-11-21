# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 950 (950) | 934 (933) | 934 (933) | 45 |
| Oportunidades | 148530 | 139636 | 137475 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 148528 | 14220344 | 1073425158 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.928 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04219 | 0.02103 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.3 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=148459, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8474000, LOW_VOLUME=4209996, PRELIM_GROSS_TOO_LOW=787599, OVER_CANDIDATE_CAP=467654, NO_POSITIVE_MARGINAL_EDGE=139897
- strike_inconsistency: NO_QUOTE=809066535, LOW_VOLUME=217675841, PRELIM_GROSS_TOO_LOW=31306635, LEG_NOT_TRADABLE=14514064, OVER_CANDIDATE_CAP=414315
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
