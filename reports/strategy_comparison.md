# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 338 (338) | 322 (322) | 322 (322) | 45 |
| Oportunidades | 57340 | 48196 | 47257 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57340 | 4657332 | 314777741 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.051 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05569 | 0.04358 | 0.02173 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.6 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57331, SUSPICIOUS_EDGE_CHECK_RULES=9
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2917807, LOW_VOLUME=1224113, PRELIM_GROSS_TOO_LOW=262673, OVER_CANDIDATE_CAP=153618, NO_POSITIVE_MARGINAL_EDGE=48276
- strike_inconsistency: NO_QUOTE=236233770, LOW_VOLUME=64573791, PRELIM_GROSS_TOO_LOW=9846121, LEG_NOT_TRADABLE=3872182, GROUPING_MISMATCH=104773
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
