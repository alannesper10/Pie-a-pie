# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 306 (306) | 290 (290) | 290 (290) | 45 |
| Oportunidades | 52724 | 43404 | 42473 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52724 | 4254629 | 287141870 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.072 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05558 | 0.04376 | 0.02186 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.3 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52724
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2667891, LOW_VOLUME=1117007, PRELIM_GROSS_TOO_LOW=239454, OVER_CANDIDATE_CAP=140276, NO_POSITIVE_MARGINAL_EDGE=43476
- strike_inconsistency: NO_QUOTE=214851053, LOW_VOLUME=59316433, PRELIM_GROSS_TOO_LOW=9100655, LEG_NOT_TRADABLE=3643416, GROUPING_MISMATCH=94563
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
