# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 85 (85) | 69 (69) | 69 (69) | 45 |
| Oportunidades | 10195 | 10331 | 10225 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10195 | 993630 | 66191762 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.201 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04552 | 0.02199 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 119.9 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10195
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=610435, LOW_VOLUME=276937, PRELIM_GROSS_TOO_LOW=54467, OVER_CANDIDATE_CAP=31569, NO_POSITIVE_MARGINAL_EDGE=10346
- strike_inconsistency: NO_QUOTE=49582095, LOW_VOLUME=13463282, PRELIM_GROSS_TOO_LOW=2119801, LEG_NOT_TRADABLE=971217, GROUPING_MISMATCH=22726
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
