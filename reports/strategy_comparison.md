# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 262 (262) | 246 (246) | 246 (246) | 45 |
| Oportunidades | 46537 | 36816 | 36121 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 46537 | 3692250 | 243609611 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.102 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05534 | 0.04412 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.6 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=46537
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2313592, LOW_VOLUME=972444, PRELIM_GROSS_TOO_LOW=206944, OVER_CANDIDATE_CAP=123348, NO_POSITIVE_MARGINAL_EDGE=36884
- strike_inconsistency: NO_QUOTE=180665753, LOW_VOLUME=51376053, PRELIM_GROSS_TOO_LOW=8065283, LEG_NOT_TRADABLE=3304801, GROUPING_MISMATCH=80564
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
