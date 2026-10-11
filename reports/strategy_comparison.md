# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 237 (237) | 221 (221) | 221 (221) | 45 |
| Oportunidades | 41066 | 33071 | 32399 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 41066 | 3347561 | 218606685 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.13 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05509 | 0.04445 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 173.3 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=41066
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2095671, LOW_VOLUME=885011, PRELIM_GROSS_TOO_LOW=186121, OVER_CANDIDATE_CAP=112264, NO_POSITIVE_MARGINAL_EDGE=33136
- strike_inconsistency: NO_QUOTE=161536436, LOW_VOLUME=46345686, PRELIM_GROSS_TOO_LOW=7406060, LEG_NOT_TRADABLE=3135943, OVER_CANDIDATE_CAP=76504
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
