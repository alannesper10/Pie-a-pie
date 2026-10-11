# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 240 (240) | 224 (224) | 224 (224) | 45 |
| Oportunidades | 41711 | 33520 | 32846 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 41711 | 3389269 | 221590354 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.126 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05512 | 0.0444 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 173.8 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=41711
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2121834, LOW_VOLUME=895844, PRELIM_GROSS_TOO_LOW=188572, OVER_CANDIDATE_CAP=113642, NO_POSITIVE_MARGINAL_EDGE=33586
- strike_inconsistency: NO_QUOTE=163824965, LOW_VOLUME=46943948, PRELIM_GROSS_TOO_LOW=7480803, LEG_NOT_TRADABLE=3156292, OVER_CANDIDATE_CAP=76859
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
