# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 189 (189) | 173 (173) | 173 (173) | 45 |
| Oportunidades | 31795 | 25894 | 25553 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 31795 | 2634905 | 169743770 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.141 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04474 | 0.02214 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 168.2 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=31795
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1643436, LOW_VOLUME=704947, PRELIM_GROSS_TOO_LOW=144650, OVER_CANDIDATE_CAP=89531, NO_POSITIVE_MARGINAL_EDGE=25939
- strike_inconsistency: NO_QUOTE=125193730, LOW_VOLUME=36211506, PRELIM_GROSS_TOO_LOW=5665460, LEG_NOT_TRADABLE=2532989, OVER_CANDIDATE_CAP=57193
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
