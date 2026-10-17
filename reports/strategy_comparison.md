# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 536 (536) | 520 (520) | 520 (520) | 45 |
| Oportunidades | 86231 | 77824 | 76612 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 86229 | 7550013 | 511491158 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.998 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05564 | 0.04308 | 0.02127 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 160.9 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=86160, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4677649, LOW_VOLUME=2035131, PRELIM_GROSS_TOO_LOW=426219, OVER_CANDIDATE_CAP=257361, NO_POSITIVE_MARGINAL_EDGE=77964
- strike_inconsistency: NO_QUOTE=378839502, LOW_VOLUME=109440147, PRELIM_GROSS_TOO_LOW=16195311, LEG_NOT_TRADABLE=6590392, OVER_CANDIDATE_CAP=177682
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
