# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 724 (724) | 708 (708) | 708 (708) | 45 |
| Oportunidades | 112533 | 105959 | 104212 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 112531 | 10217711 | 700554616 | 2412 |
| Duración media (min) | 0 | n/d | 18.82 | n/d |
| Capital por paquete (media) | 1.014 | 1.975 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0552 | 0.04273 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.4 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=112462, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6309863, LOW_VOLUME=2777833, PRELIM_GROSS_TOO_LOW=575797, OVER_CANDIDATE_CAP=348384, NO_POSITIVE_MARGINAL_EDGE=106159
- strike_inconsistency: NO_QUOTE=514775782, LOW_VOLUME=153480228, PRELIM_GROSS_TOO_LOW=22757002, LEG_NOT_TRADABLE=8935337, OVER_CANDIDATE_CAP=269025
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
