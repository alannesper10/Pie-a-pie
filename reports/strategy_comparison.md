# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 845 (845) | 829 (828) | 829 (828) | 45 |
| Oportunidades | 132577 | 123925 | 121948 | 0 |
| Net-positive | 2 | 0 | 44 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 132575 | 12162115 | 826035880 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.957 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05516 | 0.04249 | 0.02109 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 156.9 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=132506, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7500763, LOW_VOLUME=3308241, PRELIM_GROSS_TOO_LOW=691675, OVER_CANDIDATE_CAP=420425, NO_POSITIVE_MARGINAL_EDGE=124152
- strike_inconsistency: NO_QUOTE=598449473, LOW_VOLUME=188598243, PRELIM_GROSS_TOO_LOW=27594469, LEG_NOT_TRADABLE=10666123, OVER_CANDIDATE_CAP=333347
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
