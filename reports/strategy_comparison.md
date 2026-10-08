# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 67 (67) | 51 (51) | 51 (51) | 45 |
| Oportunidades | 7597 | 7635 | 7555 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7597 | 719993 | 49493587 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.288 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.0542 | 0.04626 | 0.02235 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 113.4 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7597
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=439245, LOW_VOLUME=202974, PRELIM_GROSS_TOO_LOW=40252, OVER_CANDIDATE_CAP=22648, NO_POSITIVE_MARGINAL_EDGE=7647
- strike_inconsistency: NO_QUOTE=37310707, LOW_VOLUME=9754144, PRELIM_GROSS_TOO_LOW=1535608, LEG_NOT_TRADABLE=853527, GROUPING_MISMATCH=16744
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
