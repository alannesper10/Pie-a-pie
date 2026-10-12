# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 326 (326) | 310 (310) | 310 (310) | 45 |
| Oportunidades | 55672 | 46397 | 45467 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55672 | 4503675 | 306132037 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.06 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05562 | 0.04364 | 0.02178 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.8 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55672
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2822972, LOW_VOLUME=1182569, PRELIM_GROSS_TOO_LOW=253856, OVER_CANDIDATE_CAP=148537, NO_POSITIVE_MARGINAL_EDGE=46476
- strike_inconsistency: NO_QUOTE=229962995, LOW_VOLUME=62592025, PRELIM_GROSS_TOO_LOW=9546263, LEG_NOT_TRADABLE=3787442, GROUPING_MISMATCH=100789
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
