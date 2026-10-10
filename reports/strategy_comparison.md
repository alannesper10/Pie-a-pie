# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 191 (191) | 175 (175) | 175 (175) | 45 |
| Oportunidades | 32247 | 26194 | 25852 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 32247 | 2666528 | 171846466 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.04471 | 0.02215 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 168.8 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=32247
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1663715, LOW_VOLUME=712649, PRELIM_GROSS_TOO_LOW=146473, OVER_CANDIDATE_CAP=90659, NO_POSITIVE_MARGINAL_EDGE=26239
- strike_inconsistency: NO_QUOTE=126716308, LOW_VOLUME=36663637, PRELIM_GROSS_TOO_LOW=5748212, LEG_NOT_TRADABLE=2576585, OVER_CANDIDATE_CAP=57878
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
