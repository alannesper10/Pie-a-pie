# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 105 (105) | 89 (89) | 89 (89) | 45 |
| Oportunidades | 13507 | 13329 | 13169 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 13507 | 1301382 | 87074045 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.185 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05409 | 0.04527 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 128.6 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=13507
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=801083, LOW_VOLUME=361064, PRELIM_GROSS_TOO_LOW=70519, OVER_CANDIDATE_CAP=42096, NO_POSITIVE_MARGINAL_EDGE=13346
- strike_inconsistency: NO_QUOTE=65541822, LOW_VOLUME=17654025, PRELIM_GROSS_TOO_LOW=2701787, LEG_NOT_TRADABLE=1104755, GROUPING_MISMATCH=29296
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
