# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 23 (23) | 7 (7) | 7 (7) | 45 |
| Oportunidades | 2834 | 1047 | 1035 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2834 | 97095 | 7659969 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.565 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05496 | 0.04898 | 0.02162 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.2 | 149.6 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2834
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=59384, LOW_VOLUME=27221, PRELIM_GROSS_TOO_LOW=5170, OVER_CANDIDATE_CAP=3279, NO_POSITIVE_MARGINAL_EDGE=1050
- strike_inconsistency: NO_QUOTE=5953806, LOW_VOLUME=1440953, PRELIM_GROSS_TOO_LOW=218969, LEG_NOT_TRADABLE=40301, OVER_CANDIDATE_CAP=2545
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
