# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 357 (357) | 341 (341) | 341 (341) | 45 |
| Oportunidades | 59574 | 51039 | 50066 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 59573 | 4910478 | 334244264 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05594 | 0.04353 | 0.02166 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 166.9 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=59537, SUSPICIOUS_EDGE_CHECK_RULES=36
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3070058, LOW_VOLUME=1296900, PRELIM_GROSS_TOO_LOW=276425, OVER_CANDIDATE_CAP=162303, NO_POSITIVE_MARGINAL_EDGE=51123
- strike_inconsistency: NO_QUOTE=251428786, LOW_VOLUME=68056212, PRELIM_GROSS_TOO_LOW=10321909, LEG_NOT_TRADABLE=4170885, GROUPING_MISMATCH=111150
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
