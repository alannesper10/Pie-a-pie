# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 82 (82) | 66 (66) | 66 (66) | 45 |
| Oportunidades | 9754 | 9883 | 9785 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9754 | 947159 | 63036549 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.218 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05416 | 0.04566 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 119 | 149.7 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9754
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=581500, LOW_VOLUME=264279, PRELIM_GROSS_TOO_LOW=52050, OVER_CANDIDATE_CAP=30089, NO_POSITIVE_MARGINAL_EDGE=9897
- strike_inconsistency: NO_QUOTE=47199197, LOW_VOLUME=12815272, PRELIM_GROSS_TOO_LOW=2018341, LEG_NOT_TRADABLE=951278, GROUPING_MISMATCH=21724
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
