# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 263 (263) | 247 (247) | 247 (247) | 45 |
| Oportunidades | 46732 | 36966 | 36270 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 46732 | 3705711 | 244614822 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.101 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05535 | 0.04411 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.7 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=46732
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2322166, LOW_VOLUME=975770, PRELIM_GROSS_TOO_LOW=207749, OVER_CANDIDATE_CAP=123777, NO_POSITIVE_MARGINAL_EDGE=37034
- strike_inconsistency: NO_QUOTE=181438558, LOW_VOLUME=51572301, PRELIM_GROSS_TOO_LOW=8093892, LEG_NOT_TRADABLE=3311715, GROUPING_MISMATCH=80879
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
