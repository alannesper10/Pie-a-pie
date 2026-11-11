# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 913 (913) | 897 (896) | 897 (896) | 45 |
| Oportunidades | 143406 | 134094 | 131962 | 0 |
| Net-positive | 2 | 0 | 50 | 0 |
| Ejecutables | 2 | 0 | 46 | 0 |
| Descartadas | 143404 | 13440220 | 943550868 | 2412 |
| Duración media (min) | 0 | n/d | 17.8 | n/d |
| Capital por paquete (media) | 1.014 | 1.931 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05502 | 0.04217 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 157.1 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=143335, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8127079, LOW_VOLUME=3836339, PRELIM_GROSS_TOO_LOW=754015, OVER_CANDIDATE_CAP=455449, NO_POSITIVE_MARGINAL_EDGE=134347
- strike_inconsistency: NO_QUOTE=693481980, LOW_VOLUME=206666327, PRELIM_GROSS_TOO_LOW=30058188, LEG_NOT_TRADABLE=12521240, OVER_CANDIDATE_CAP=394944
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
