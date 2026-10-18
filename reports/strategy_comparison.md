# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 610 (610) | 594 (594) | 594 (594) | 45 |
| Oportunidades | 99142 | 88892 | 87344 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 99140 | 8640612 | 588320903 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.994 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05537 | 0.04306 | 0.02122 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 162.5 | 149.6 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=99071, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5360019, LOW_VOLUME=2325965, PRELIM_GROSS_TOO_LOW=486528, OVER_CANDIDATE_CAP=293025, NO_POSITIVE_MARGINAL_EDGE=89063
- strike_inconsistency: NO_QUOTE=433499192, LOW_VOLUME=127928670, PRELIM_GROSS_TOO_LOW=19039954, LEG_NOT_TRADABLE=7348233, OVER_CANDIDATE_CAP=220906
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
