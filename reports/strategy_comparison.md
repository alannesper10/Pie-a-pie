# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 77 (77) | 61 (61) | 61 (61) | 45 |
| Oportunidades | 8990 | 9134 | 9043 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8990 | 870942 | 57782285 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.247 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05423 | 0.04589 | 0.02215 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 116.8 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8990
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=533653, LOW_VOLUME=243973, PRELIM_GROSS_TOO_LOW=48032, OVER_CANDIDATE_CAP=27560, NO_POSITIVE_MARGINAL_EDGE=9147
- strike_inconsistency: NO_QUOTE=43206744, LOW_VOLUME=11759048, PRELIM_GROSS_TOO_LOW=1848918, LEG_NOT_TRADABLE=919426, GROUPING_MISMATCH=20064
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
