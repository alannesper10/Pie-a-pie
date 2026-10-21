# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 698 (698) | 682 (682) | 682 (682) | 45 |
| Oportunidades | 109318 | 102071 | 100329 | 0 |
| Net-positive | 2 | 0 | 16 | 0 |
| Ejecutables | 2 | 0 | 15 | 0 |
| Descartadas | 109316 | 9832515 | 675183144 | 2412 |
| Duración media (min) | 0 | n/d | 26.11 | n/d |
| Capital por paquete (media) | 1.014 | 1.984 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04288 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.6 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=109247, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6079630, LOW_VOLUME=2665905, PRELIM_GROSS_TOO_LOW=553385, OVER_CANDIDATE_CAP=334324, NO_POSITIVE_MARGINAL_EDGE=102259
- strike_inconsistency: NO_QUOTE=496856003, LOW_VOLUME=147376204, PRELIM_GROSS_TOO_LOW=21758043, LEG_NOT_TRADABLE=8610449, OVER_CANDIDATE_CAP=257327
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
