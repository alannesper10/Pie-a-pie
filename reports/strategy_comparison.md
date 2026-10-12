# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 315 (315) | 299 (299) | 299 (299) | 45 |
| Oportunidades | 54024 | 44750 | 43822 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 54024 | 4366178 | 296065612 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.068 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0556 | 0.04371 | 0.02183 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.5 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=54024
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2737209, LOW_VOLUME=1146479, PRELIM_GROSS_TOO_LOW=245875, OVER_CANDIDATE_CAP=144032, NO_POSITIVE_MARGINAL_EDGE=44826
- strike_inconsistency: NO_QUOTE=222006520, LOW_VOLUME=60828197, PRELIM_GROSS_TOO_LOW=9288858, LEG_NOT_TRADABLE=3705901, GROUPING_MISMATCH=97344
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
