# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 238 (238) | 222 (222) | 222 (222) | 45 |
| Oportunidades | 41278 | 33221 | 32546 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 41278 | 3361492 | 219601265 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.128 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0551 | 0.04443 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 173.4 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=41278
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2104402, LOW_VOLUME=888651, PRELIM_GROSS_TOO_LOW=186930, OVER_CANDIDATE_CAP=112719, NO_POSITIVE_MARGINAL_EDGE=33286
- strike_inconsistency: NO_QUOTE=162300604, LOW_VOLUME=46543571, PRELIM_GROSS_TOO_LOW=7431071, LEG_NOT_TRADABLE=3142854, OVER_CANDIDATE_CAP=76632
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
