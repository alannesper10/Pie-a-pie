# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 290 (290) | 274 (274) | 274 (274) | 45 |
| Oportunidades | 50665 | 41006 | 40110 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50665 | 4054548 | 271239486 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.079 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05551 | 0.04384 | 0.02194 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 174.7 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50665
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2543973, LOW_VOLUME=1063491, PRELIM_GROSS_TOO_LOW=228523, OVER_CANDIDATE_CAP=133719, NO_POSITIVE_MARGINAL_EDGE=41077
- strike_inconsistency: NO_QUOTE=202135462, LOW_VOLUME=56569110, PRELIM_GROSS_TOO_LOW=8786875, LEG_NOT_TRADABLE=3528254, GROUPING_MISMATCH=89619
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
