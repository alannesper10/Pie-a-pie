# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 70 (70) | 54 (54) | 54 (54) | 45 |
| Oportunidades | 7995 | 8084 | 7996 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7995 | 765003 | 51291375 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.282 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05421 | 0.04621 | 0.02227 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 114.2 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7995
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=467312, LOW_VOLUME=215268, PRELIM_GROSS_TOO_LOW=42617, OVER_CANDIDATE_CAP=24101, NO_POSITIVE_MARGINAL_EDGE=8097
- strike_inconsistency: NO_QUOTE=38441989, LOW_VOLUME=10305571, PRELIM_GROSS_TOO_LOW=1627059, LEG_NOT_TRADABLE=874559, GROUPING_MISMATCH=17740
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
