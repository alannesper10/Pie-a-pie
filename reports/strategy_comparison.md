# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 89 (89) | 73 (73) | 73 (73) | 45 |
| Oportunidades | 10794 | 10931 | 10801 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10794 | 1055701 | 70406047 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.193 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05405 | 0.04544 | 0.02193 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 121.3 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10794
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=648942, LOW_VOLUME=294025, PRELIM_GROSS_TOO_LOW=57583, OVER_CANDIDATE_CAP=33558, NO_POSITIVE_MARGINAL_EDGE=10946
- strike_inconsistency: NO_QUOTE=52783078, LOW_VOLUME=14325759, PRELIM_GROSS_TOO_LOW=2237677, LEG_NOT_TRADABLE=1000148, OVER_CANDIDATE_CAP=24213
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
