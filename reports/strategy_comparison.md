# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 41 (41) | 25 (25) | 25 (25) | 45 |
| Oportunidades | 4668 | 3744 | 3701 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4668 | 350513 | 25408451 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.561 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.04912 | 0.02198 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 113.9 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4668
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=212535, LOW_VOLUME=99675, PRELIM_GROSS_TOO_LOW=19392, OVER_CANDIDATE_CAP=11312, NO_POSITIVE_MARGINAL_EDGE=3748
- strike_inconsistency: NO_QUOTE=19609268, LOW_VOLUME=4886447, PRELIM_GROSS_TOO_LOW=743793, LEG_NOT_TRADABLE=149015, GROUPING_MISMATCH=8245
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
