# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 242 (242) | 226 (226) | 226 (226) | 45 |
| Oportunidades | 42157 | 33820 | 33145 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 42157 | 3417027 | 223583054 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.123 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05514 | 0.04436 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 174.2 | 149.6 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=42157
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2139266, LOW_VOLUME=902998, PRELIM_GROSS_TOO_LOW=190230, OVER_CANDIDATE_CAP=114573, NO_POSITIVE_MARGINAL_EDGE=33886
- strike_inconsistency: NO_QUOTE=165348794, LOW_VOLUME=47347796, PRELIM_GROSS_TOO_LOW=7531081, LEG_NOT_TRADABLE=3169859, OVER_CANDIDATE_CAP=77083
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
