# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 533 (533) | 517 (517) | 517 (517) | 45 |
| Oportunidades | 85571 | 77374 | 76162 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 85569 | 7501402 | 508273776 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05565 | 0.0431 | 0.02127 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 160.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=85500, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4647187, LOW_VOLUME=2022220, PRELIM_GROSS_TOO_LOW=423548, OVER_CANDIDATE_CAP=255550, NO_POSITIVE_MARGINAL_EDGE=77514
- strike_inconsistency: NO_QUOTE=376693865, LOW_VOLUME=108533785, PRELIM_GROSS_TOO_LOW=16059721, LEG_NOT_TRADABLE=6563767, OVER_CANDIDATE_CAP=175939
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
