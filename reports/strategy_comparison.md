# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 590 (590) | 574 (574) | 574 (574) | 45 |
| Oportunidades | 96160 | 85901 | 84527 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 96158 | 8371221 | 568045527 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.013 | 1.994 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05542 | 0.04306 | 0.02123 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 163 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=96089, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5191708, LOW_VOLUME=2254915, PRELIM_GROSS_TOO_LOW=471093, OVER_CANDIDATE_CAP=284560, NO_POSITIVE_MARGINAL_EDGE=86064
- strike_inconsistency: NO_QUOTE=418671801, LOW_VOLUME=123352109, PRELIM_GROSS_TOO_LOW=18423147, LEG_NOT_TRADABLE=7110710, OVER_CANDIDATE_CAP=213436
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
