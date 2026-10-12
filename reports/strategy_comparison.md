# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 337 (337) | 321 (321) | 321 (321) | 45 |
| Oportunidades | 57218 | 48047 | 47108 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57218 | 4644454 | 313774062 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.052 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05568 | 0.04358 | 0.02173 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.8 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57210, SUSPICIOUS_EDGE_CHECK_RULES=8
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2909907, LOW_VOLUME=1220545, PRELIM_GROSS_TOO_LOW=261967, OVER_CANDIDATE_CAP=153202, NO_POSITIVE_MARGINAL_EDGE=48126
- strike_inconsistency: NO_QUOTE=235445906, LOW_VOLUME=64391393, PRELIM_GROSS_TOO_LOW=9820625, LEG_NOT_TRADABLE=3864956, GROUPING_MISMATCH=104441
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
