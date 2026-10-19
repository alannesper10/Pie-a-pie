# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 638 (638) | 622 (622) | 622 (622) | 45 |
| Oportunidades | 102285 | 93088 | 91430 | 0 |
| Net-positive | 2 | 0 | 4 | 0 |
| Ejecutables | 2 | 0 | 3 | 0 |
| Descartadas | 102283 | 8997557 | 617229898 | 2412 |
| Duración media (min) | 0 | n/d | 0 | n/d |
| Capital por paquete (media) | 1.014 | 1.993 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05533 | 0.04302 | 0.02122 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 11 | n/d |
| Oport. por ciclo | 160.3 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 89.36 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 10.64 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.19 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.022 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=102214, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=5579539, LOW_VOLUME=2424832, PRELIM_GROSS_TOO_LOW=505442, OVER_CANDIDATE_CAP=304689, NO_POSITIVE_MARGINAL_EDGE=93263
- strike_inconsistency: NO_QUOTE=455482535, LOW_VOLUME=133582982, PRELIM_GROSS_TOO_LOW=19778362, LEG_NOT_TRADABLE=7860683, OVER_CANDIDATE_CAP=228553
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
