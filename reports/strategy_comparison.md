# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 448 (448) | 432 (432) | 432 (432) | 45 |
| Oportunidades | 70700 | 64657 | 63540 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 70698 | 6176922 | 423436418 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.018 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05592 | 0.04323 | 0.02143 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 157.8 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=70629, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3828774, LOW_VOLUME=1661106, PRELIM_GROSS_TOO_LOW=349554, OVER_CANDIDATE_CAP=208566, NO_POSITIVE_MARGINAL_EDGE=64769
- strike_inconsistency: NO_QUOTE=317846150, LOW_VOLUME=86680276, PRELIM_GROSS_TOO_LOW=12965811, LEG_NOT_TRADABLE=5602703, GROUPING_MISMATCH=140729
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
