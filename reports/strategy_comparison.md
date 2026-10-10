# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 149 (149) | 133 (133) | 133 (133) | 45 |
| Oportunidades | 22247 | 19909 | 19640 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 22247 | 1995120 | 128158533 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.173 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05457 | 0.04525 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 149.3 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=22247
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1239527, LOW_VOLUME=541544, PRELIM_GROSS_TOO_LOW=108644, OVER_CANDIDATE_CAP=66021, NO_POSITIVE_MARGINAL_EDGE=19941
- strike_inconsistency: NO_QUOTE=95080107, LOW_VOLUME=26857243, PRELIM_GROSS_TOO_LOW=4200542, LEG_NOT_TRADABLE=1912033, OVER_CANDIDATE_CAP=44796
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
