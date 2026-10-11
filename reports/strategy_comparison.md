# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 228 (228) | 212 (212) | 212 (212) | 45 |
| Oportunidades | 39309 | 31727 | 31083 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 39309 | 3221210 | 209637144 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.136 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.055 | 0.04455 | 0.02201 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.4 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=39309
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2016676, LOW_VOLUME=851704, PRELIM_GROSS_TOO_LOW=178981, OVER_CANDIDATE_CAP=108239, NO_POSITIVE_MARGINAL_EDGE=31786
- strike_inconsistency: NO_QUOTE=154651665, LOW_VOLUME=44554881, PRELIM_GROSS_TOO_LOW=7179594, LEG_NOT_TRADABLE=3074044, OVER_CANDIDATE_CAP=75218
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
