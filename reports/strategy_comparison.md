# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 120 (120) | 104 (104) | 104 (104) | 45 |
| Oportunidades | 16423 | 15570 | 15394 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 16423 | 1533367 | 102516475 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.188 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05419 | 0.0453 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 136.9 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=16423
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=946267, LOW_VOLUME=422810, PRELIM_GROSS_TOO_LOW=83035, OVER_CANDIDATE_CAP=50317, NO_POSITIVE_MARGINAL_EDGE=15593
- strike_inconsistency: NO_QUOTE=77472978, LOW_VOLUME=20596036, PRELIM_GROSS_TOO_LOW=3164026, LEG_NOT_TRADABLE=1200515, GROUPING_MISMATCH=34171
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
