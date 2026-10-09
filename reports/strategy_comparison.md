# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 106 (106) | 90 (90) | 90 (90) | 45 |
| Oportunidades | 13695 | 13479 | 13319 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 13695 | 1316735 | 88124713 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.185 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04526 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 129.2 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=13695
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=810588, LOW_VOLUME=365232, PRELIM_GROSS_TOO_LOW=71354, OVER_CANDIDATE_CAP=42650, NO_POSITIVE_MARGINAL_EDGE=13496
- strike_inconsistency: NO_QUOTE=66354185, LOW_VOLUME=17855469, PRELIM_GROSS_TOO_LOW=2731628, LEG_NOT_TRADABLE=1111045, GROUPING_MISMATCH=29621
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
