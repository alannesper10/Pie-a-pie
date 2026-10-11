# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 224 (224) | 208 (208) | 208 (208) | 45 |
| Oportunidades | 38591 | 31127 | 30552 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 38591 | 3163979 | 205603347 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.137 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05497 | 0.04457 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.3 | 149.6 | 146.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=38591
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1980793, LOW_VOLUME=836682, PRELIM_GROSS_TOO_LOW=175707, OVER_CANDIDATE_CAP=106536, NO_POSITIVE_MARGINAL_EDGE=31186
- strike_inconsistency: NO_QUOTE=151566441, LOW_VOLUME=43754729, PRELIM_GROSS_TOO_LOW=7064224, LEG_NOT_TRADABLE=3044180, OVER_CANDIDATE_CAP=73968
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
