# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 969 (969) | 953 (952) | 953 (952) | 45 |
| Oportunidades | 151368 | 142473 | 140286 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 151366 | 14609397 | 1129598974 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.927 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05487 | 0.04223 | 0.02102 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.2 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=151297, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8648190, LOW_VOLUME=4396574, PRELIM_GROSS_TOO_LOW=803433, OVER_CANDIDATE_CAP=473648, NO_POSITIVE_MARGINAL_EDGE=142742
- strike_inconsistency: NO_QUOTE=858463441, LOW_VOLUME=222722052, PRELIM_GROSS_TOO_LOW=31924365, LEG_NOT_TRADABLE=15606078, OVER_CANDIDATE_CAP=424636
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
