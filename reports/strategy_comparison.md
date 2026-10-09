# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 83 (83) | 67 (67) | 67 (67) | 45 |
| Oportunidades | 9900 | 10032 | 9933 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9900 | 962557 | 64087887 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.212 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05414 | 0.04561 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 119.3 | 149.7 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9900
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=591116, LOW_VOLUME=268436, PRELIM_GROSS_TOO_LOW=52862, OVER_CANDIDATE_CAP=30585, NO_POSITIVE_MARGINAL_EDGE=10047
- strike_inconsistency: NO_QUOTE=47996909, LOW_VOLUME=13027127, PRELIM_GROSS_TOO_LOW=2052765, LEG_NOT_TRADABLE=957705, GROUPING_MISMATCH=22056
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
