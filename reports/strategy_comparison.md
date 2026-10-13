# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 349 (349) | 333 (333) | 333 (333) | 45 |
| Oportunidades | 58651 | 49842 | 48887 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 58650 | 4802001 | 326035088 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0558 | 0.04353 | 0.02169 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 168.1 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=58630, SUSPICIOUS_EDGE_CHECK_RULES=20
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3005626, LOW_VOLUME=1264940, PRELIM_GROSS_TOO_LOW=270623, OVER_CANDIDATE_CAP=158392, NO_POSITIVE_MARGINAL_EDGE=49925
- strike_inconsistency: NO_QUOTE=244939875, LOW_VOLUME=66589973, PRELIM_GROSS_TOO_LOW=10133044, LEG_NOT_TRADABLE=4112129, GROUPING_MISMATCH=108442
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
