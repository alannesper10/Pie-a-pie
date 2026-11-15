# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 932 (932) | 916 (915) | 916 (915) | 45 |
| Oportunidades | 146091 | 136939 | 134792 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 146089 | 13838939 | 1025097105 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.927 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05495 | 0.04216 | 0.02104 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.8 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=146020, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8305803, LOW_VOLUME=4025403, PRELIM_GROSS_TOO_LOW=771481, OVER_CANDIDATE_CAP=461766, NO_POSITIVE_MARGINAL_EDGE=137197
- strike_inconsistency: NO_QUOTE=766886388, LOW_VOLUME=212755870, PRELIM_GROSS_TOO_LOW=30729945, LEG_NOT_TRADABLE=13880938, OVER_CANDIDATE_CAP=405813
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
