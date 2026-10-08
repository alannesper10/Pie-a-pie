# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 46 (46) | 30 (30) | 30 (30) | 45 |
| Oportunidades | 5032 | 4494 | 4451 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 5032 | 420579 | 30132998 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.477 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05448 | 0.04822 | 0.0221 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.4 | 149.8 | 148.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=5032
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=254888, LOW_VOLUME=119827, PRELIM_GROSS_TOO_LOW=23902, OVER_CANDIDATE_CAP=12895, NO_POSITIVE_MARGINAL_EDGE=4498
- strike_inconsistency: NO_QUOTE=23254730, LOW_VOLUME=5749902, PRELIM_GROSS_TOO_LOW=880461, LEG_NOT_TRADABLE=224686, GROUPING_MISMATCH=9870
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
