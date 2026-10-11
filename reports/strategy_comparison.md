# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 278 (278) | 262 (262) | 262 (262) | 45 |
| Oportunidades | 49131 | 39214 | 38382 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 49131 | 3903850 | 259721545 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.086 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05546 | 0.04392 | 0.02201 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 176.7 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=49131
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2448620, LOW_VOLUME=1024951, PRELIM_GROSS_TOO_LOW=219915, OVER_CANDIDATE_CAP=129429, NO_POSITIVE_MARGINAL_EDGE=39283
- strike_inconsistency: NO_QUOTE=193123372, LOW_VOLUME=54425805, PRELIM_GROSS_TOO_LOW=8534586, LEG_NOT_TRADABLE=3427650, GROUPING_MISMATCH=85768
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
