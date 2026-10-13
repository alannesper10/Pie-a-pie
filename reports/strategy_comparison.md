# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 350 (350) | 334 (334) | 334 (334) | 45 |
| Oportunidades | 58764 | 49990 | 49035 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 58763 | 4815590 | 327066983 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05582 | 0.04353 | 0.02169 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 167.9 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=58741, SUSPICIOUS_EDGE_CHECK_RULES=22
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3013716, LOW_VOLUME=1268968, PRELIM_GROSS_TOO_LOW=271334, OVER_CANDIDATE_CAP=158847, NO_POSITIVE_MARGINAL_EDGE=50074
- strike_inconsistency: NO_QUOTE=245755612, LOW_VOLUME=66773460, PRELIM_GROSS_TOO_LOW=10157724, LEG_NOT_TRADABLE=4119264, GROUPING_MISMATCH=108784
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
