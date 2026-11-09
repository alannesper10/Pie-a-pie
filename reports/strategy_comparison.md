# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 907 (907) | 891 (890) | 891 (890) | 45 |
| Oportunidades | 142761 | 133195 | 131075 | 0 |
| Net-positive | 2 | 0 | 48 | 0 |
| Ejecutables | 2 | 0 | 44 | 0 |
| Descartadas | 142759 | 13325465 | 935988016 | 2412 |
| Duración media (min) | 0 | n/d | 18.44 | n/d |
| Capital por paquete (media) | 1.014 | 1.933 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05505 | 0.04219 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 637.3 | n/d |
| Oport. por ciclo | 157.4 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=142690, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8078026, LOW_VOLUME=3779528, PRELIM_GROSS_TOO_LOW=749008, OVER_CANDIDATE_CAP=453809, NO_POSITIVE_MARGINAL_EDGE=133447
- strike_inconsistency: NO_QUOTE=687483891, LOW_VOLUME=205358885, PRELIM_GROSS_TOO_LOW=29881233, LEG_NOT_TRADABLE=12446989, OVER_CANDIDATE_CAP=391871
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
