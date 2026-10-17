# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 524 (524) | 508 (508) | 508 (508) | 45 |
| Oportunidades | 83569 | 76030 | 74817 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 83567 | 7354277 | 498612776 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.001 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05569 | 0.0431 | 0.02129 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=83498, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4555250, LOW_VOLUME=1983072, PRELIM_GROSS_TOO_LOW=415597, OVER_CANDIDATE_CAP=249898, NO_POSITIVE_MARGINAL_EDGE=76166
- strike_inconsistency: NO_QUOTE=370259805, LOW_VOLUME=105795723, PRELIM_GROSS_TOO_LOW=15660518, LEG_NOT_TRADABLE=6483550, OVER_CANDIDATE_CAP=170770
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
