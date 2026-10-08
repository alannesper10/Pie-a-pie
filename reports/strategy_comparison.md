# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 45 (45) | 29 (29) | 29 (29) | 45 |
| Oportunidades | 4919 | 4344 | 4301 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 4919 | 406607 | 29211621 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.494 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05449 | 0.0484 | 0.02208 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 109.3 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=4919
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=246416, LOW_VOLUME=115836, PRELIM_GROSS_TOO_LOW=23117, OVER_CANDIDATE_CAP=12457, NO_POSITIVE_MARGINAL_EDGE=4348
- strike_inconsistency: NO_QUOTE=22612197, LOW_VOLUME=5553726, PRELIM_GROSS_TOO_LOW=851867, LEG_NOT_TRADABLE=171360, GROUPING_MISMATCH=9545
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
