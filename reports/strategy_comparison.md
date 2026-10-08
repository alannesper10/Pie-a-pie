# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 62 (62) | 46 (46) | 46 (46) | 45 |
| Oportunidades | 6943 | 6887 | 6820 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 6943 | 646523 | 45904080 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.31 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05426 | 0.04645 | 0.02246 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 112 | 149.7 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=6943
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=393676, LOW_VOLUME=182798, PRELIM_GROSS_TOO_LOW=36314, OVER_CANDIDATE_CAP=20247, NO_POSITIVE_MARGINAL_EDGE=6897
- strike_inconsistency: NO_QUOTE=35106814, LOW_VOLUME=8820079, PRELIM_GROSS_TOO_LOW=1372572, LEG_NOT_TRADABLE=569141, GROUPING_MISMATCH=15084
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
