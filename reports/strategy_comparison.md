# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 889 (889) | 873 (872) | 873 (872) | 45 |
| Oportunidades | 139791 | 130505 | 128397 | 0 |
| Net-positive | 2 | 0 | 45 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 139789 | 12946123 | 881762218 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.941 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05509 | 0.04223 | 0.02106 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 157.2 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=139720, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=7904515, LOW_VOLUME=3603964, PRELIM_GROSS_TOO_LOW=732178, OVER_CANDIDATE_CAP=447474, NO_POSITIVE_MARGINAL_EDGE=130749
- strike_inconsistency: NO_QUOTE=639886532, LOW_VOLUME=199966535, PRELIM_GROSS_TOO_LOW=29181381, LEG_NOT_TRADABLE=11941304, OVER_CANDIDATE_CAP=370451
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
