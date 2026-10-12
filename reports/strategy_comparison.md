# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 300 (300) | 284 (284) | 284 (284) | 45 |
| Oportunidades | 51893 | 42506 | 41577 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 51893 | 4179894 | 281207355 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.073 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05556 | 0.04378 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 173 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=51893
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2621674, LOW_VOLUME=1097047, PRELIM_GROSS_TOO_LOW=235366, OVER_CANDIDATE_CAP=137659, NO_POSITIVE_MARGINAL_EDGE=42577
- strike_inconsistency: NO_QUOTE=210105121, LOW_VOLUME=58292480, PRELIM_GROSS_TOO_LOW=8981535, LEG_NOT_TRADABLE=3601800, GROUPING_MISMATCH=92709
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
