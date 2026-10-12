# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 334 (334) | 318 (318) | 318 (318) | 45 |
| Oportunidades | 56821 | 47597 | 46659 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56821 | 4605756 | 311050188 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.055 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05565 | 0.04361 | 0.02174 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.1 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56816, SUSPICIOUS_EDGE_CHECK_RULES=5
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2886120, LOW_VOLUME=1209881, PRELIM_GROSS_TOO_LOW=259833, OVER_CANDIDATE_CAP=151954, NO_POSITIVE_MARGINAL_EDGE=47676
- strike_inconsistency: NO_QUOTE=233371881, LOW_VOLUME=63840800, PRELIM_GROSS_TOO_LOW=9744529, LEG_NOT_TRADABLE=3843950, GROUPING_MISMATCH=103445
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
