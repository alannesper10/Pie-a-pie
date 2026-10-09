# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 102 (102) | 86 (86) | 86 (86) | 45 |
| Oportunidades | 12958 | 12879 | 12720 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12958 | 1255420 | 83927850 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04532 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 127 | 149.8 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12958
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=772546, LOW_VOLUME=348683, PRELIM_GROSS_TOO_LOW=68020, OVER_CANDIDATE_CAP=40433, NO_POSITIVE_MARGINAL_EDGE=12896
- strike_inconsistency: NO_QUOTE=63112830, LOW_VOLUME=17047335, PRELIM_GROSS_TOO_LOW=2612498, LEG_NOT_TRADABLE=1085765, GROUPING_MISMATCH=28321
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
