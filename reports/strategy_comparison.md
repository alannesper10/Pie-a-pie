# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 108 (108) | 92 (92) | 92 (92) | 45 |
| Oportunidades | 14077 | 13778 | 13615 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 14077 | 1347448 | 90226119 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.185 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05411 | 0.04524 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 130.3 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=14077
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=829612, LOW_VOLUME=373554, PRELIM_GROSS_TOO_LOW=72985, OVER_CANDIDATE_CAP=43802, NO_POSITIVE_MARGINAL_EDGE=13796
- strike_inconsistency: NO_QUOTE=67978647, LOW_VOLUME=18258531, PRELIM_GROSS_TOO_LOW=2791495, LEG_NOT_TRADABLE=1123625, GROUPING_MISMATCH=30271
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
