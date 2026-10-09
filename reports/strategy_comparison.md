# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 135 (135) | 119 (119) | 119 (119) | 45 |
| Oportunidades | 19461 | 17812 | 17588 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 19461 | 1771042 | 113712906 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.179 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05437 | 0.04528 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 144.2 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=19461
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1097217, LOW_VOLUME=484145, PRELIM_GROSS_TOO_LOW=96199, OVER_CANDIDATE_CAP=58226, NO_POSITIVE_MARGINAL_EDGE=17841
- strike_inconsistency: NO_QUOTE=84665335, LOW_VOLUME=23455651, PRELIM_GROSS_TOO_LOW=3674274, LEG_NOT_TRADABLE=1822392, GROUPING_MISMATCH=39046
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
