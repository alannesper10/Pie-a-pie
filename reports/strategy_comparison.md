# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 758 (758) | 742 (741) | 742 (741) | 45 |
| Oportunidades | 117037 | 110903 | 109135 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 117035 | 10728282 | 734623790 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.963 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05518 | 0.04254 | 0.02114 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.4 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=116966, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6616682, LOW_VOLUME=2922335, PRELIM_GROSS_TOO_LOW=607171, OVER_CANDIDATE_CAP=366601, NO_POSITIVE_MARGINAL_EDGE=111108
- strike_inconsistency: NO_QUOTE=539083846, LOW_VOLUME=161507705, PRELIM_GROSS_TOO_LOW=24024360, LEG_NOT_TRADABLE=9363964, OVER_CANDIDATE_CAP=291120
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
