# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 342 (342) | 326 (326) | 326 (326) | 45 |
| Oportunidades | 57822 | 48794 | 47850 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57822 | 4709064 | 318847681 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.049 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05572 | 0.04356 | 0.02172 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.1 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57809, SUSPICIOUS_EDGE_CHECK_RULES=13
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2949507, LOW_VOLUME=1238429, PRELIM_GROSS_TOO_LOW=265538, OVER_CANDIDATE_CAP=155299, NO_POSITIVE_MARGINAL_EDGE=48876
- strike_inconsistency: NO_QUOTE=239435167, LOW_VOLUME=65308049, PRELIM_GROSS_TOO_LOW=9949574, LEG_NOT_TRADABLE=3900245, GROUPING_MISMATCH=106101
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
