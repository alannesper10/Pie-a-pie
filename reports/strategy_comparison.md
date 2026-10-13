# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 370 (370) | 354 (354) | 354 (354) | 45 |
| Oportunidades | 61127 | 52986 | 52010 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61125 | 5085464 | 347526439 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.044 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05607 | 0.04351 | 0.02161 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.2 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=61074, SUSPICIOUS_EDGE_CHECK_RULES=51
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3174249, LOW_VOLUME=1347269, PRELIM_GROSS_TOO_LOW=286447, OVER_CANDIDATE_CAP=169356, NO_POSITIVE_MARGINAL_EDGE=53073
- strike_inconsistency: NO_QUOTE=261795143, LOW_VOLUME=70392502, PRELIM_GROSS_TOO_LOW=10636673, LEG_NOT_TRADABLE=4425757, GROUPING_MISMATCH=115465
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
