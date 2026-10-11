# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 264 (264) | 248 (248) | 248 (248) | 45 |
| Oportunidades | 46920 | 37115 | 36417 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 46920 | 3719103 | 245619916 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.101 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05536 | 0.0441 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.7 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=46920
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2330699, LOW_VOLUME=979070, PRELIM_GROSS_TOO_LOW=208579, OVER_CANDIDATE_CAP=124191, NO_POSITIVE_MARGINAL_EDGE=37184
- strike_inconsistency: NO_QUOTE=182211593, LOW_VOLUME=51767620, PRELIM_GROSS_TOO_LOW=8122943, LEG_NOT_TRADABLE=3318752, GROUPING_MISMATCH=81194
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
