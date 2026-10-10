# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 186 (186) | 170 (170) | 170 (170) | 45 |
| Oportunidades | 31112 | 25447 | 25108 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 31112 | 2587098 | 166589454 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.143 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04479 | 0.02212 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 167.3 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=31112
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1612797, LOW_VOLUME=693214, PRELIM_GROSS_TOO_LOW=141875, OVER_CANDIDATE_CAP=87839, NO_POSITIVE_MARGINAL_EDGE=25489
- strike_inconsistency: NO_QUOTE=122913332, LOW_VOLUME=35526676, PRELIM_GROSS_TOO_LOW=5544218, LEG_NOT_TRADABLE=2467563, OVER_CANDIDATE_CAP=56204
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
