# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 709 (709) | 693 (693) | 693 (693) | 45 |
| Oportunidades | 110701 | 103719 | 101978 | 0 |
| Net-positive | 2 | 0 | 27 | 0 |
| Ejecutables | 2 | 0 | 26 | 0 |
| Descartadas | 110699 | 9994851 | 687024826 | 2412 |
| Duración media (min) | 0 | n/d | 23.07 | n/d |
| Capital por paquete (media) | 1.014 | 1.981 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04283 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.1 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110630, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6175284, LOW_VOLUME=2714391, PRELIM_GROSS_TOO_LOW=562913, OVER_CANDIDATE_CAP=340282, NO_POSITIVE_MARGINAL_EDGE=103909
- strike_inconsistency: NO_QUOTE=505518010, LOW_VOLUME=150025165, PRELIM_GROSS_TOO_LOW=22143164, LEG_NOT_TRADABLE=8746741, OVER_CANDIDATE_CAP=261570
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
