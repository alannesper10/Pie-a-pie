# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 30 (30) | 14 (14) | 14 (14) | 45 |
| Oportunidades | 3664 | 2096 | 2074 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3664 | 195703 | 15288402 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.579 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05468 | 0.04936 | 0.02141 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122.1 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3664
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=119341, LOW_VOLUME=55042, PRELIM_GROSS_TOO_LOW=10359, OVER_CANDIDATE_CAP=6692, NO_POSITIVE_MARGINAL_EDGE=2100
- strike_inconsistency: NO_QUOTE=11911073, LOW_VOLUME=2855317, PRELIM_GROSS_TOO_LOW=429916, LEG_NOT_TRADABLE=79732, OVER_CANDIDATE_CAP=5574
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
