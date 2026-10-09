# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 104 (104) | 88 (88) | 88 (88) | 45 |
| Oportunidades | 13321 | 13179 | 13019 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 13321 | 1286062 | 86023297 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.185 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05409 | 0.04528 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 128.1 | 149.8 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=13321
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=791564, LOW_VOLUME=356952, PRELIM_GROSS_TOO_LOW=69684, OVER_CANDIDATE_CAP=41539, NO_POSITIVE_MARGINAL_EDGE=13196
- strike_inconsistency: NO_QUOTE=64730298, LOW_VOLUME=17451770, PRELIM_GROSS_TOO_LOW=2671977, LEG_NOT_TRADABLE=1098350, GROUPING_MISMATCH=28971
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
