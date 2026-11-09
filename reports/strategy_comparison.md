# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 909 (909) | 893 (892) | 893 (892) | 45 |
| Oportunidades | 142935 | 133494 | 131372 | 0 |
| Net-positive | 2 | 0 | 48 | 0 |
| Ejecutables | 2 | 0 | 44 | 0 |
| Descartadas | 142933 | 13362311 | 938824465 | 2412 |
| Duración media (min) | 0 | n/d | 18.44 | n/d |
| Capital por paquete (media) | 1.014 | 1.932 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05504 | 0.04218 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 637.3 | n/d |
| Oport. por ciclo | 157.2 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=142864, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8093722, LOW_VOLUME=3797895, PRELIM_GROSS_TOO_LOW=750576, OVER_CANDIDATE_CAP=454300, NO_POSITIVE_MARGINAL_EDGE=133747
- strike_inconsistency: NO_QUOTE=689682186, LOW_VOLUME=205913637, PRELIM_GROSS_TOO_LOW=29939268, LEG_NOT_TRADABLE=12470477, OVER_CANDIDATE_CAP=392763
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
