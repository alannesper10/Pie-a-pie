# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 341 (341) | 325 (325) | 325 (325) | 45 |
| Oportunidades | 57695 | 48645 | 47704 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 57695 | 4696089 | 317825253 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.049 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05571 | 0.04356 | 0.02172 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 169.2 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=57683, SUSPICIOUS_EDGE_CHECK_RULES=12
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2941559, LOW_VOLUME=1234848, PRELIM_GROSS_TOO_LOW=264812, OVER_CANDIDATE_CAP=154876, NO_POSITIVE_MARGINAL_EDGE=48726
- strike_inconsistency: NO_QUOTE=238630267, LOW_VOLUME=65124266, PRELIM_GROSS_TOO_LOW=9923479, LEG_NOT_TRADABLE=3893281, GROUPING_MISMATCH=105769
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
