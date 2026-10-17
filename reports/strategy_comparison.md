# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 538 (538) | 522 (522) | 522 (522) | 45 |
| Oportunidades | 86676 | 78124 | 76912 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 86674 | 7582368 | 513637242 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.998 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05563 | 0.04308 | 0.02126 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.1 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=86605, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4697950, LOW_VOLUME=2043722, PRELIM_GROSS_TOO_LOW=427980, OVER_CANDIDATE_CAP=258567, NO_POSITIVE_MARGINAL_EDGE=78264
- strike_inconsistency: NO_QUOTE=380275220, LOW_VOLUME=110039553, PRELIM_GROSS_TOO_LOW=16286490, LEG_NOT_TRADABLE=6608145, OVER_CANDIDATE_CAP=178760
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
