# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 340 (340) | 324 (324) | 324 (324) | 45 |
| Oportunidades | 57576 | 48496 | 47554 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57576 | 4683117 | 316801950 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.05 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0557 | 0.04357 | 0.02172 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.3 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57565, SUSPICIOUS_EDGE_CHECK_RULES=11
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2933612, LOW_VOLUME=1231246, PRELIM_GROSS_TOO_LOW=264104, OVER_CANDIDATE_CAP=154454, NO_POSITIVE_MARGINAL_EDGE=48576
- strike_inconsistency: NO_QUOTE=237825508, LOW_VOLUME=64939224, PRELIM_GROSS_TOO_LOW=9897604, LEG_NOT_TRADABLE=3886354, GROUPING_MISMATCH=105437
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
