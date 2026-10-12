# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 307 (307) | 291 (291) | 291 (291) | 45 |
| Oportunidades | 52870 | 43554 | 42623 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52870 | 4267053 | 288130973 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.072 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05559 | 0.04376 | 0.02186 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.2 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52870
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2675591, LOW_VOLUME=1120305, PRELIM_GROSS_TOO_LOW=240140, OVER_CANDIDATE_CAP=140725, NO_POSITIVE_MARGINAL_EDGE=43626
- strike_inconsistency: NO_QUOTE=215642286, LOW_VOLUME=59485900, PRELIM_GROSS_TOO_LOW=9121463, LEG_NOT_TRADABLE=3650361, GROUPING_MISMATCH=94872
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
