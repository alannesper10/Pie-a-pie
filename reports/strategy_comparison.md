# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 113 (113) | 97 (97) | 97 (97) | 45 |
| Oportunidades | 15039 | 14525 | 14360 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 15039 | 1424273 | 95488818 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05412 | 0.04526 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 133.1 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=15039
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=877446, LOW_VOLUME=394141, PRELIM_GROSS_TOO_LOW=77114, OVER_CANDIDATE_CAP=46592, NO_POSITIVE_MARGINAL_EDGE=14545
- strike_inconsistency: NO_QUOTE=72050524, LOW_VOLUME=19264173, PRELIM_GROSS_TOO_LOW=2941544, LEG_NOT_TRADABLE=1155045, GROUPING_MISMATCH=31896
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
