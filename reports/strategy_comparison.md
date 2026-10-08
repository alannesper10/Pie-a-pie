# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 63 (63) | 47 (47) | 47 (47) | 45 |
| Oportunidades | 7073 | 7037 | 6964 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7073 | 660926 | 46635493 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.302 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05425 | 0.04636 | 0.02245 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 112.3 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7073
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=402543, LOW_VOLUME=186803, PRELIM_GROSS_TOO_LOW=37084, OVER_CANDIDATE_CAP=20735, NO_POSITIVE_MARGINAL_EDGE=7047
- strike_inconsistency: NO_QUOTE=35608872, LOW_VOLUME=9009268, PRELIM_GROSS_TOO_LOW=1406132, LEG_NOT_TRADABLE=574967, GROUPING_MISMATCH=15416
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
