# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 323 (323) | 307 (307) | 307 (307) | 45 |
| Oportunidades | 55215 | 45949 | 45017 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55215 | 4465830 | 303756519 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.063 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04366 | 0.0218 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.9 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55215
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2799450, LOW_VOLUME=1172599, PRELIM_GROSS_TOO_LOW=251628, OVER_CANDIDATE_CAP=147262, NO_POSITIVE_MARGINAL_EDGE=46026
- strike_inconsistency: NO_QUOTE=228155552, LOW_VOLUME=62125471, PRELIM_GROSS_TOO_LOW=9472891, LEG_NOT_TRADABLE=3761295, GROUPING_MISMATCH=99816
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
