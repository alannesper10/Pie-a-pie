# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 99 (99) | 83 (83) | 83 (83) | 45 |
| Oportunidades | 12435 | 12429 | 12272 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12435 | 1209362 | 80801421 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05409 | 0.04534 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 125.6 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12435
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=744019, LOW_VOLUME=336158, PRELIM_GROSS_TOO_LOW=65517, OVER_CANDIDATE_CAP=38822, NO_POSITIVE_MARGINAL_EDGE=12446
- strike_inconsistency: NO_QUOTE=60712796, LOW_VOLUME=16431310, PRELIM_GROSS_TOO_LOW=2524110, LEG_NOT_TRADABLE=1065992, GROUPING_MISMATCH=27346
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
