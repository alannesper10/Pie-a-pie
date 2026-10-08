# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 28 (28) | 12 (12) | 12 (12) | 45 |
| Oportunidades | 3430 | 1796 | 1776 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 3430 | 167561 | 13146001 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.565 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05473 | 0.04913 | 0.02142 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 122.5 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=3430
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=102235, LOW_VOLUME=47114, PRELIM_GROSS_TOO_LOW=8855, OVER_CANDIDATE_CAP=5720, NO_POSITIVE_MARGINAL_EDGE=1800
- strike_inconsistency: NO_QUOTE=10242470, LOW_VOLUME=2453873, PRELIM_GROSS_TOO_LOW=370384, LEG_NOT_TRADABLE=68623, OVER_CANDIDATE_CAP=4831
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
