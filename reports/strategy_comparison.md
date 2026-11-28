# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 971 (971) | 955 (954) | 955 (954) | 45 |
| Oportunidades | 151744 | 142771 | 140584 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 151742 | 14652827 | 1140285666 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.927 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05487 | 0.04223 | 0.02102 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.3 | 149.7 | 147.4 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=151673, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8668343, LOW_VOLUME=4416882, PRELIM_GROSS_TOO_LOW=805074, OVER_CANDIDATE_CAP=474293, NO_POSITIVE_MARGINAL_EDGE=143042
- strike_inconsistency: NO_QUOTE=868444920, LOW_VOLUME=223324490, PRELIM_GROSS_TOO_LOW=31987426, LEG_NOT_TRADABLE=15643490, OVER_CANDIDATE_CAP=425756
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
