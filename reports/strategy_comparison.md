# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 269 (269) | 253 (253) | 253 (253) | 45 |
| Oportunidades | 47847 | 37864 | 37151 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 47847 | 3785847 | 250655710 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.096 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05541 | 0.04404 | 0.02205 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.9 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=47847
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2373238, LOW_VOLUME=995565, PRELIM_GROSS_TOO_LOW=212752, OVER_CANDIDATE_CAP=126145, NO_POSITIVE_MARGINAL_EDGE=37934
- strike_inconsistency: NO_QUOTE=186081387, LOW_VOLUME=52744082, PRELIM_GROSS_TOO_LOW=8273380, LEG_NOT_TRADABLE=3354359, GROUPING_MISMATCH=82761
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
