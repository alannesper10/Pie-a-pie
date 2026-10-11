# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 241 (241) | 225 (225) | 225 (225) | 45 |
| Oportunidades | 41933 | 33670 | 32995 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 41933 | 3403153 | 222586715 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.125 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05513 | 0.04439 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 174 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=41933
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2130552, LOW_VOLUME=899422, PRELIM_GROSS_TOO_LOW=189405, OVER_CANDIDATE_CAP=114105, NO_POSITIVE_MARGINAL_EDGE=33736
- strike_inconsistency: NO_QUOTE=164586956, LOW_VOLUME=47145981, PRELIM_GROSS_TOO_LOW=7505815, LEG_NOT_TRADABLE=3163033, OVER_CANDIDATE_CAP=76966
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
