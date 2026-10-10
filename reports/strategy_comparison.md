# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 176 (176) | 160 (160) | 160 (160) | 45 |
| Oportunidades | 28722 | 23950 | 23614 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 28722 | 2428065 | 156126148 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.152 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04494 | 0.02207 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 163.2 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=28722
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1511444, LOW_VOLUME=653302, PRELIM_GROSS_TOO_LOW=132829, OVER_CANDIDATE_CAP=82213, NO_POSITIVE_MARGINAL_EDGE=23991
- strike_inconsistency: NO_QUOTE=115362563, LOW_VOLUME=33214753, PRELIM_GROSS_TOO_LOW=5168098, LEG_NOT_TRADABLE=2250830, OVER_CANDIDATE_CAP=53213
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
