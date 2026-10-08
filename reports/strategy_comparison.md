# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 66 (66) | 50 (50) | 50 (50) | 45 |
| Oportunidades | 7466 | 7485 | 7408 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7466 | 705090 | 48838683 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.29 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05421 | 0.04627 | 0.02238 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 113.1 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7466
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=429973, LOW_VOLUME=198896, PRELIM_GROSS_TOO_LOW=39456, OVER_CANDIDATE_CAP=22166, NO_POSITIVE_MARGINAL_EDGE=7497
- strike_inconsistency: NO_QUOTE=36880523, LOW_VOLUME=9568664, PRELIM_GROSS_TOO_LOW=1504030, LEG_NOT_TRADABLE=846720, GROUPING_MISMATCH=16412
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
