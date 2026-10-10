# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 179 (179) | 163 (163) | 163 (163) | 45 |
| Oportunidades | 29451 | 24398 | 24062 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 29451 | 2475667 | 159250830 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.149 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05492 | 0.04488 | 0.02209 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 164.5 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=29451
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1541621, LOW_VOLUME=665377, PRELIM_GROSS_TOO_LOW=135595, OVER_CANDIDATE_CAP=83877, NO_POSITIVE_MARGINAL_EDGE=24440
- strike_inconsistency: NO_QUOTE=117618936, LOW_VOLUME=33906082, PRELIM_GROSS_TOO_LOW=5278120, LEG_NOT_TRADABLE=2315489, OVER_CANDIDATE_CAP=54081
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
