# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 376 (376) | 360 (360) | 360 (360) | 45 |
| Oportunidades | 61861 | 53884 | 52908 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61859 | 5165661 | 353640844 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.042 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05611 | 0.04348 | 0.02159 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 164.5 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61802, SUSPICIOUS_EDGE_CHECK_RULES=57
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3222515, LOW_VOLUME=1369941, PRELIM_GROSS_TOO_LOW=290998, OVER_CANDIDATE_CAP=172468, NO_POSITIVE_MARGINAL_EDGE=53973
- strike_inconsistency: NO_QUOTE=266550985, LOW_VOLUME=71462512, PRELIM_GROSS_TOO_LOW=10786207, LEG_NOT_TRADABLE=4560139, GROUPING_MISMATCH=117451
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
