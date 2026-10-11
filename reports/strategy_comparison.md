# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 280 (280) | 264 (264) | 264 (264) | 45 |
| Oportunidades | 49398 | 39512 | 38677 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 49398 | 3929556 | 261433515 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.085 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05547 | 0.04391 | 0.02199 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 176.4 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=49398
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2465037, LOW_VOLUME=1031431, PRELIM_GROSS_TOO_LOW=221406, OVER_CANDIDATE_CAP=130116, NO_POSITIVE_MARGINAL_EDGE=39581
- strike_inconsistency: NO_QUOTE=194400094, LOW_VOLUME=54794989, PRELIM_GROSS_TOO_LOW=8580653, LEG_NOT_TRADABLE=3445654, GROUPING_MISMATCH=86407
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
