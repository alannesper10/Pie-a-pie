# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 252 (252) | 236 (236) | 236 (236) | 45 |
| Oportunidades | 44402 | 35316 | 34639 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 44402 | 3555410 | 233565315 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.112 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05523 | 0.04424 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 176.2 | 149.6 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=44402
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2226554, LOW_VOLUME=938277, PRELIM_GROSS_TOO_LOW=198664, OVER_CANDIDATE_CAP=119053, NO_POSITIVE_MARGINAL_EDGE=35384
- strike_inconsistency: NO_QUOTE=172979700, LOW_VOLUME=49365868, PRELIM_GROSS_TOO_LOW=7791295, LEG_NOT_TRADABLE=3236954, OVER_CANDIDATE_CAP=78287
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
