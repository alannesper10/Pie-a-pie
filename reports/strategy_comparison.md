# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 347 (347) | 331 (331) | 331 (331) | 45 |
| Oportunidades | 58424 | 49543 | 48589 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 58424 | 4774869 | 323972480 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05578 | 0.04353 | 0.0217 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 168.4 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=58406, SUSPICIOUS_EDGE_CHECK_RULES=18
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2989453, LOW_VOLUME=1256940, PRELIM_GROSS_TOO_LOW=269172, OVER_CANDIDATE_CAP=157505, NO_POSITIVE_MARGINAL_EDGE=49626
- strike_inconsistency: NO_QUOTE=243310211, LOW_VOLUME=66223591, PRELIM_GROSS_TOO_LOW=10082280, LEG_NOT_TRADABLE=4097974, GROUPING_MISMATCH=107765
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
