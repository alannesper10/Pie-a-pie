# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 403 (403) | 387 (387) | 387 (387) | 45 |
| Oportunidades | 65101 | 57923 | 56904 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 65099 | 5536143 | 377954855 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.031 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05612 | 0.04335 | 0.02151 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 161.5 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=65030, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3446516, LOW_VOLUME=1474905, PRELIM_GROSS_TOO_LOW=312254, OVER_CANDIDATE_CAP=185467, NO_POSITIVE_MARGINAL_EDGE=58021
- strike_inconsistency: NO_QUOTE=284530437, LOW_VOLUME=76500432, PRELIM_GROSS_TOO_LOW=11522444, LEG_NOT_TRADABLE=5097547, GROUPING_MISMATCH=126209
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
