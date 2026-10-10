# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 214 (214) | 198 (198) | 198 (198) | 45 |
| Oportunidades | 36745 | 29634 | 29121 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 36745 | 3017320 | 195411010 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.14 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05495 | 0.04464 | 0.02209 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.7 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=36745
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1887917, LOW_VOLUME=799569, PRELIM_GROSS_TOO_LOW=166979, OVER_CANDIDATE_CAP=102167, NO_POSITIVE_MARGINAL_EDGE=29688
- strike_inconsistency: NO_QUOTE=143890333, LOW_VOLUME=41665033, PRELIM_GROSS_TOO_LOW=6721274, LEG_NOT_TRADABLE=2969579, OVER_CANDIDATE_CAP=69827
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
