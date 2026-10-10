# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 202 (202) | 186 (186) | 186 (186) | 45 |
| Oportunidades | 34458 | 27839 | 27444 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 34458 | 2836605 | 183404929 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.137 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.04466 | 0.02216 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.6 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=34458
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1772533, LOW_VOLUME=754436, PRELIM_GROSS_TOO_LOW=156568, OVER_CANDIDATE_CAP=96501, NO_POSITIVE_MARGINAL_EDGE=27889
- strike_inconsistency: NO_QUOTE=135111056, LOW_VOLUME=39088890, PRELIM_GROSS_TOO_LOW=6232805, LEG_NOT_TRADABLE=2819783, OVER_CANDIDATE_CAP=63239
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
