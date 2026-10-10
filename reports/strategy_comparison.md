# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 216 (216) | 200 (200) | 200 (200) | 45 |
| Oportunidades | 37133 | 29931 | 29389 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 37133 | 3046932 | 197467882 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05495 | 0.04463 | 0.02208 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.9 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=37133
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1906748, LOW_VOLUME=806968, PRELIM_GROSS_TOO_LOW=168719, OVER_CANDIDATE_CAP=103090, NO_POSITIVE_MARGINAL_EDGE=29987
- strike_inconsistency: NO_QUOTE=145430316, LOW_VOLUME=42091071, PRELIM_GROSS_TOO_LOW=6792731, LEG_NOT_TRADABLE=2986884, OVER_CANDIDATE_CAP=70948
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
