# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 711 (711) | 695 (695) | 695 (695) | 45 |
| Oportunidades | 110940 | 104018 | 102277 | 0 |
| Net-positive | 2 | 0 | 29 | 0 |
| Ejecutables | 2 | 0 | 28 | 0 |
| Descartadas | 110938 | 10024201 | 689206979 | 2412 |
| Duración media (min) | 0 | n/d | 22.16 | n/d |
| Capital por paquete (media) | 1.014 | 1.98 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04282 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110869, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6192819, LOW_VOLUME=2722995, PRELIM_GROSS_TOO_LOW=564584, OVER_CANDIDATE_CAP=341317, NO_POSITIVE_MARGINAL_EDGE=104209
- strike_inconsistency: NO_QUOTE=507119722, LOW_VOLUME=150503377, PRELIM_GROSS_TOO_LOW=22218929, LEG_NOT_TRADABLE=8771451, OVER_CANDIDATE_CAP=262414
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
