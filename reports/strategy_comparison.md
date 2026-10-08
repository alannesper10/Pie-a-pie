# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 48 (48) | 32 (32) | 32 (32) | 45 |
| Oportunidades | 5258 | 4794 | 4747 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5258 | 448561 | 32220889 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.445 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05446 | 0.04787 | 0.0222 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.5 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5258
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=271895, LOW_VOLUME=127768, PRELIM_GROSS_TOO_LOW=25475, OVER_CANDIDATE_CAP=13793, NO_POSITIVE_MARGINAL_EDGE=4798
- strike_inconsistency: NO_QUOTE=24877518, LOW_VOLUME=6143248, PRELIM_GROSS_TOO_LOW=939357, LEG_NOT_TRADABLE=235936, GROUPING_MISMATCH=10520
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
