# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 291 (291) | 275 (275) | 275 (275) | 45 |
| Oportunidades | 50788 | 41156 | 40258 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50788 | 4066905 | 272229962 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.078 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05551 | 0.04384 | 0.02193 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 174.5 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50788
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2551693, LOW_VOLUME=1066731, PRELIM_GROSS_TOO_LOW=229206, OVER_CANDIDATE_CAP=134106, NO_POSITIVE_MARGINAL_EDGE=41227
- strike_inconsistency: NO_QUOTE=202923292, LOW_VOLUME=56743643, PRELIM_GROSS_TOO_LOW=8806462, LEG_NOT_TRADABLE=3536141, GROUPING_MISMATCH=89928
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
