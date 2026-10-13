# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 346 (346) | 330 (330) | 330 (330) | 45 |
| Oportunidades | 58308 | 49393 | 48440 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 58308 | 4761321 | 322943116 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05576 | 0.04353 | 0.02171 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 168.5 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=58291, SUSPICIOUS_EDGE_CHECK_RULES=17
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2981371, LOW_VOLUME=1252944, PRELIM_GROSS_TOO_LOW=268448, OVER_CANDIDATE_CAP=157066, NO_POSITIVE_MARGINAL_EDGE=49476
- strike_inconsistency: NO_QUOTE=242497893, LOW_VOLUME=66040295, PRELIM_GROSS_TOO_LOW=10056342, LEG_NOT_TRADABLE=4090962, GROUPING_MISMATCH=107429
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
