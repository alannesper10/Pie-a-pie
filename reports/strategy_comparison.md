# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 562 (562) | 546 (546) | 546 (546) | 45 |
| Oportunidades | 91334 | 81709 | 80413 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 91332 | 7963209 | 539150105 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.995 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05549 | 0.04308 | 0.02122 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=91263, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4938837, LOW_VOLUME=2142819, PRELIM_GROSS_TOO_LOW=449025, OVER_CANDIDATE_CAP=271786, NO_POSITIVE_MARGINAL_EDGE=81864
- strike_inconsistency: NO_QUOTE=397516742, LOW_VOLUME=116850789, PRELIM_GROSS_TOO_LOW=17491475, LEG_NOT_TRADABLE=6833415, OVER_CANDIDATE_CAP=196783
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
