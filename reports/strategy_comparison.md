# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 753 (753) | 737 (736) | 737 (736) | 45 |
| Oportunidades | 116288 | 110153 | 108389 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 116286 | 10649990 | 730478560 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.965 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05518 | 0.04256 | 0.02115 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.4 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=116217, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6568779, LOW_VOLUME=2900933, PRELIM_GROSS_TOO_LOW=602536, OVER_CANDIDATE_CAP=363730, NO_POSITIVE_MARGINAL_EDGE=110358
- strike_inconsistency: NO_QUOTE=536315620, LOW_VOLUME=160397182, PRELIM_GROSS_TOO_LOW=23828630, LEG_NOT_TRADABLE=9298411, OVER_CANDIDATE_CAP=288287
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
