# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 58 (58) | 42 (42) | 42 (42) | 45 |
| Oportunidades | 6449 | 6290 | 6227 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 6449 | 589358 | 42491989 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.34 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05431 | 0.04677 | 0.02252 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 111.2 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=6449
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=358369, LOW_VOLUME=167069, PRELIM_GROSS_TOO_LOW=33190, OVER_CANDIDATE_CAP=18337, NO_POSITIVE_MARGINAL_EDGE=6297
- strike_inconsistency: NO_QUOTE=32593193, LOW_VOLUME=8075496, PRELIM_GROSS_TOO_LOW=1245143, LEG_NOT_TRADABLE=545823, GROUPING_MISMATCH=13770
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
