# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 900 (900) | 884 (883) | 884 (883) | 45 |
| Oportunidades | 141830 | 132149 | 130041 | 0 |
| Net-positive | 2 | 0 | 48 | 0 |
| Ejecutables | 2 | 0 | 44 | 0 |
| Descartadas | 141828 | 13187630 | 900093592 | 2412 |
| Duración media (min) | 0 | n/d | 18.44 | n/d |
| Capital por paquete (media) | 1.014 | 1.935 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05507 | 0.0422 | 0.02106 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 637.3 | n/d |
| Oport. por ciclo | 157.6 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=141759, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8016537, LOW_VOLUME=3713963, PRELIM_GROSS_TOO_LOW=742741, OVER_CANDIDATE_CAP=452033, NO_POSITIVE_MARGINAL_EDGE=132397
- strike_inconsistency: NO_QUOTE=653937987, LOW_VOLUME=203610523, PRELIM_GROSS_TOO_LOW=29649964, LEG_NOT_TRADABLE=12086373, OVER_CANDIDATE_CAP=387201
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
