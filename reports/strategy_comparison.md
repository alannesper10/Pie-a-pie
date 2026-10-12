# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 330 (330) | 314 (314) | 314 (314) | 45 |
| Oportunidades | 56265 | 46997 | 46062 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56265 | 4554530 | 308873291 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.057 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05562 | 0.04362 | 0.02176 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.5 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56264, SUSPICIOUS_EDGE_CHECK_RULES=1
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2854487, LOW_VOLUME=1196070, PRELIM_GROSS_TOO_LOW=256880, OVER_CANDIDATE_CAP=150225, NO_POSITIVE_MARGINAL_EDGE=47076
- strike_inconsistency: NO_QUOTE=231947036, LOW_VOLUME=63218365, PRELIM_GROSS_TOO_LOW=9645862, LEG_NOT_TRADABLE=3815902, GROUPING_MISMATCH=102117
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
