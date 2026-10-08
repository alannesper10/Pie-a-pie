# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 64 (64) | 48 (48) | 48 (48) | 45 |
| Oportunidades | 7201 | 7186 | 7114 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 7201 | 675575 | 47368940 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.298 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05424 | 0.04633 | 0.02243 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 112.5 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=7201
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=411637, LOW_VOLUME=190830, PRELIM_GROSS_TOO_LOW=37866, OVER_CANDIDATE_CAP=21209, NO_POSITIVE_MARGINAL_EDGE=7197
- strike_inconsistency: NO_QUOTE=36114038, LOW_VOLUME=9197109, PRELIM_GROSS_TOO_LOW=1439941, LEG_NOT_TRADABLE=580793, GROUPING_MISMATCH=15748
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
