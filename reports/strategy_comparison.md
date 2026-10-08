# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 72 (72) | 56 (56) | 56 (56) | 45 |
| Oportunidades | 8264 | 8384 | 8296 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8264 | 795094 | 52756901 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.274 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05423 | 0.04615 | 0.02225 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 114.8 | 149.7 | 148.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8264
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=486132, LOW_VOLUME=223463, PRELIM_GROSS_TOO_LOW=44155, OVER_CANDIDATE_CAP=25077, NO_POSITIVE_MARGINAL_EDGE=8397
- strike_inconsistency: NO_QUOTE=39434597, LOW_VOLUME=10703171, PRELIM_GROSS_TOO_LOW=1687904, LEG_NOT_TRADABLE=887392, GROUPING_MISMATCH=18404
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
