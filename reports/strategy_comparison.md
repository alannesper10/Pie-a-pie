# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 466 (466) | 450 (450) | 450 (450) | 45 |
| Oportunidades | 72975 | 67350 | 66231 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 72973 | 6442391 | 440934937 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.008 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05584 | 0.04315 | 0.0214 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.6 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=72904, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3987951, LOW_VOLUME=1738206, PRELIM_GROSS_TOO_LOW=365293, OVER_CANDIDATE_CAP=216846, NO_POSITIVE_MARGINAL_EDGE=67468
- strike_inconsistency: NO_QUOTE=330593683, LOW_VOLUME=90692677, PRELIM_GROSS_TOO_LOW=13559162, LEG_NOT_TRADABLE=5733466, GROUPING_MISMATCH=146424
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
