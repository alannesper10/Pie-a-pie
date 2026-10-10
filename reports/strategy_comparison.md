# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 217 (217) | 201 (201) | 201 (201) | 45 |
| Oportunidades | 37314 | 30081 | 29534 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 37314 | 3061665 | 198490697 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.139 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05495 | 0.04462 | 0.02207 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=37314
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1916115, LOW_VOLUME=810651, PRELIM_GROSS_TOO_LOW=169592, OVER_CANDIDATE_CAP=103541, NO_POSITIVE_MARGINAL_EDGE=30137
- strike_inconsistency: NO_QUOTE=146197720, LOW_VOLUME=42304222, PRELIM_GROSS_TOO_LOW=6826544, LEG_NOT_TRADABLE=2994376, OVER_CANDIDATE_CAP=71419
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
