# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 132 (132) | 116 (116) | 116 (116) | 45 |
| Oportunidades | 18935 | 17362 | 17146 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 18935 | 1723388 | 111327743 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.175 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05434 | 0.04522 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 143.4 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=18935
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1066973, LOW_VOLUME=471731, PRELIM_GROSS_TOO_LOW=93582, OVER_CANDIDATE_CAP=56721, NO_POSITIVE_MARGINAL_EDGE=17391
- strike_inconsistency: NO_QUOTE=83061144, LOW_VOLUME=22798218, PRELIM_GROSS_TOO_LOW=3572289, LEG_NOT_TRADABLE=1803155, GROUPING_MISMATCH=38071
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
