# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 246 (246) | 230 (230) | 230 (230) | 45 |
| Oportunidades | 43042 | 34417 | 33745 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 43042 | 3472463 | 227574090 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.117 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05517 | 0.0443 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 175 | 149.6 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=43042
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2174166, LOW_VOLUME=917194, PRELIM_GROSS_TOO_LOW=193582, OVER_CANDIDATE_CAP=116409, NO_POSITIVE_MARGINAL_EDGE=34484
- strike_inconsistency: NO_QUOTE=168400419, LOW_VOLUME=48155277, PRELIM_GROSS_TOO_LOW=7633622, LEG_NOT_TRADABLE=3196870, OVER_CANDIDATE_CAP=77553
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
