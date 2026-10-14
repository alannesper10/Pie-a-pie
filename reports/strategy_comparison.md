# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 437 (437) | 421 (421) | 421 (421) | 45 |
| Oportunidades | 69401 | 63010 | 61963 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 69399 | 6015586 | 411521275 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.021 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05597 | 0.04324 | 0.02144 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 158.8 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=69330, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3732823, LOW_VOLUME=1613329, PRELIM_GROSS_TOO_LOW=340703, OVER_CANDIDATE_CAP=202942, NO_POSITIVE_MARGINAL_EDGE=63120
- strike_inconsistency: NO_QUOTE=309510602, LOW_VOLUME=83586982, PRELIM_GROSS_TOO_LOW=12574048, LEG_NOT_TRADABLE=5518805, GROUPING_MISMATCH=137182
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
