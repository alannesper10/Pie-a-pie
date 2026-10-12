# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 319 (319) | 303 (303) | 303 (303) | 45 |
| Oportunidades | 54613 | 45350 | 44419 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 54613 | 4415722 | 300059127 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.066 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0556 | 0.04369 | 0.02182 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.2 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=54613
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2768205, LOW_VOLUME=1159411, PRELIM_GROSS_TOO_LOW=248745, OVER_CANDIDATE_CAP=145614, NO_POSITIVE_MARGINAL_EDGE=45426
- strike_inconsistency: NO_QUOTE=225220347, LOW_VOLUME=61490117, PRELIM_GROSS_TOO_LOW=9376277, LEG_NOT_TRADABLE=3733726, GROUPING_MISMATCH=98580
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
