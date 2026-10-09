# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 123 (123) | 107 (107) | 107 (107) | 45 |
| Oportunidades | 17072 | 16018 | 15830 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 17072 | 1580569 | 105142403 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.181 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05424 | 0.04523 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 138.8 | 149.7 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=17072
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=976239, LOW_VOLUME=434961, PRELIM_GROSS_TOO_LOW=85652, OVER_CANDIDATE_CAP=51943, NO_POSITIVE_MARGINAL_EDGE=16043
- strike_inconsistency: NO_QUOTE=79155100, LOW_VOLUME=21157075, PRELIM_GROSS_TOO_LOW=3263487, LEG_NOT_TRADABLE=1481312, GROUPING_MISMATCH=35146
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
