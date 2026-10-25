# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 839 (839) | 823 (822) | 823 (822) | 45 |
| Oportunidades | 131740 | 123025 | 121082 | 0 |
| Net-positive | 2 | 0 | 43 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 131738 | 12076956 | 819744103 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.959 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05517 | 0.04253 | 0.0211 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 157 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=131669, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7449388, LOW_VOLUME=3284461, PRELIM_GROSS_TOO_LOW=686354, OVER_CANDIDATE_CAP=417594, NO_POSITIVE_MARGINAL_EDGE=123252
- strike_inconsistency: NO_QUOTE=594154584, LOW_VOLUME=186907992, PRELIM_GROSS_TOO_LOW=27391948, LEG_NOT_TRADABLE=10567124, OVER_CANDIDATE_CAP=331128
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
