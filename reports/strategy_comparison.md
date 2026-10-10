# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 172 (172) | 156 (156) | 156 (156) | 45 |
| Oportunidades | 27726 | 23351 | 23015 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 27726 | 2364546 | 151961264 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.154 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05486 | 0.04499 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 161.2 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=27726
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1471331, LOW_VOLUME=637115, PRELIM_GROSS_TOO_LOW=129238, OVER_CANDIDATE_CAP=79806, NO_POSITIVE_MARGINAL_EDGE=23391
- strike_inconsistency: NO_QUOTE=112358126, LOW_VOLUME=32288037, PRELIM_GROSS_TOO_LOW=5023708, LEG_NOT_TRADABLE=2164555, OVER_CANDIDATE_CAP=52055
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
