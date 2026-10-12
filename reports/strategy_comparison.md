# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 295 (295) | 279 (279) | 279 (279) | 45 |
| Oportunidades | 51269 | 41756 | 40852 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 51269 | 4117201 | 276216217 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.076 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05554 | 0.04381 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 173.8 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=51269
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2582847, LOW_VOLUME=1080262, PRELIM_GROSS_TOO_LOW=231954, OVER_CANDIDATE_CAP=135632, NO_POSITIVE_MARGINAL_EDGE=41827
- strike_inconsistency: NO_QUOTE=206110401, LOW_VOLUME=57431118, PRELIM_GROSS_TOO_LOW=8885815, LEG_NOT_TRADABLE=3565789, GROUPING_MISMATCH=91164
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
