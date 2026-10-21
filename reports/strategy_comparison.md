# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 717 (717) | 701 (701) | 701 (701) | 45 |
| Oportunidades | 111658 | 104913 | 103171 | 0 |
| Net-positive | 2 | 0 | 35 | 0 |
| Ejecutables | 2 | 0 | 34 | 0 |
| Descartadas | 111656 | 10112583 | 695000967 | 2412 |
| Duración media (min) | 0 | n/d | 18.43 | n/d |
| Capital por paquete (media) | 1.014 | 1.978 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05521 | 0.04277 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.7 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=111587, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6246080, LOW_VOLUME=2748299, PRELIM_GROSS_TOO_LOW=569573, OVER_CANDIDATE_CAP=344641, NO_POSITIVE_MARGINAL_EDGE=105109
- strike_inconsistency: NO_QUOTE=511279295, LOW_VOLUME=151809576, PRELIM_GROSS_TOO_LOW=22466095, LEG_NOT_TRADABLE=8846682, OVER_CANDIDATE_CAP=265488
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
