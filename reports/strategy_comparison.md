# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 343 (343) | 327 (327) | 327 (327) | 45 |
| Oportunidades | 57935 | 48943 | 48000 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57935 | 4722063 | 319870186 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.048 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05573 | 0.04355 | 0.02172 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 168.9 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57921, SUSPICIOUS_EDGE_CHECK_RULES=14
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2957457, LOW_VOLUME=1242023, PRELIM_GROSS_TOO_LOW=266259, OVER_CANDIDATE_CAP=155739, NO_POSITIVE_MARGINAL_EDGE=49026
- strike_inconsistency: NO_QUOTE=240240006, LOW_VOLUME=65491460, PRELIM_GROSS_TOO_LOW=9976099, LEG_NOT_TRADABLE=3907253, GROUPING_MISMATCH=106433
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
