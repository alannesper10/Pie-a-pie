# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 392 (392) | 376 (376) | 376 (376) | 45 |
| Oportunidades | 63811 | 56276 | 55278 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 63809 | 5382683 | 366450961 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.034 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05616 | 0.04338 | 0.02154 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.8 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=63740, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3354620, LOW_VOLUME=1430500, PRELIM_GROSS_TOO_LOW=303433, OVER_CANDIDATE_CAP=180088, NO_POSITIVE_MARGINAL_EDGE=56372
- strike_inconsistency: NO_QUOTE=276020480, LOW_VOLUME=74258206, PRELIM_GROSS_TOO_LOW=11201438, LEG_NOT_TRADABLE=4676240, GROUPING_MISMATCH=122744
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
