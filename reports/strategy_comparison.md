# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 518 (518) | 502 (502) | 502 (502) | 45 |
| Oportunidades | 82297 | 75133 | 73942 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 82295 | 7255529 | 492112516 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05572 | 0.04309 | 0.0213 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 158.9 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=82226, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4493288, LOW_VOLUME=1957212, PRELIM_GROSS_TOO_LOW=410240, OVER_CANDIDATE_CAP=246100, NO_POSITIVE_MARGINAL_EDGE=75267
- strike_inconsistency: NO_QUOTE=365867247, LOW_VOLUME=104024997, PRELIM_GROSS_TOO_LOW=15385097, LEG_NOT_TRADABLE=6428676, OVER_CANDIDATE_CAP=166981
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
