# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 729 (729) | 713 (713) | 713 (713) | 45 |
| Oportunidades | 113221 | 106707 | 104959 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 113219 | 10293859 | 706092093 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.973 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.0552 | 0.0427 | 0.02118 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 155.3 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=113150, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6355902, LOW_VOLUME=2799110, PRELIM_GROSS_TOO_LOW=580365, OVER_CANDIDATE_CAP=351234, NO_POSITIVE_MARGINAL_EDGE=106908
- strike_inconsistency: NO_QUOTE=518680465, LOW_VOLUME=154820344, PRELIM_GROSS_TOO_LOW=22980459, LEG_NOT_TRADABLE=8999153, OVER_CANDIDATE_CAP=272078
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
