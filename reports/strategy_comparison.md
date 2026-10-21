# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 712 (712) | 696 (696) | 696 (696) | 45 |
| Oportunidades | 111059 | 104166 | 102427 | 0 |
| Net-positive | 2 | 0 | 30 | 0 |
| Ejecutables | 2 | 0 | 29 | 0 |
| Descartadas | 111057 | 10038849 | 690305435 | 2412 |
| Duración media (min) | 0 | n/d | 20.86 | n/d |
| Capital por paquete (media) | 1.014 | 1.98 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05522 | 0.04281 | 0.02119 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=110988, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6201606, LOW_VOLUME=2727241, PRELIM_GROSS_TOO_LOW=565395, OVER_CANDIDATE_CAP=341875, NO_POSITIVE_MARGINAL_EDGE=104359
- strike_inconsistency: NO_QUOTE=507930841, LOW_VOLUME=150736422, PRELIM_GROSS_TOO_LOW=22259117, LEG_NOT_TRADABLE=8784625, OVER_CANDIDATE_CAP=262889
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
