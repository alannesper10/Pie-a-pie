# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 966 (966) | 950 (949) | 950 (949) | 45 |
| Oportunidades | 150883 | 142023 | 139838 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 150881 | 14544408 | 1117042683 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.927 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05487 | 0.04222 | 0.02102 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.2 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=150812, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8618290, LOW_VOLUME=4365895, PRELIM_GROSS_TOO_LOW=800970, OVER_CANDIDATE_CAP=472649, NO_POSITIVE_MARGINAL_EDGE=142292
- strike_inconsistency: NO_QUOTE=846919349, LOW_VOLUME=221852688, PRELIM_GROSS_TOO_LOW=31840159, LEG_NOT_TRADABLE=15550672, OVER_CANDIDATE_CAP=423195
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
