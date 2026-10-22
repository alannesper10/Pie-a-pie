# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 747 (747) | 731 (730) | 731 (730) | 45 |
| Oportunidades | 115424 | 109255 | 107492 | 0 |
| Net-positive | 2 | 0 | 42 | 0 |
| Ejecutables | 2 | 0 | 41 | 0 |
| Descartadas | 115422 | 10557057 | 724045515 | 2412 |
| Duración media (min) | 0 | n/d | 20.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.967 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05519 | 0.0426 | 0.02115 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 28.28 | n/d |
| Oport. por ciclo | 154.5 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=115353, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=6512576, LOW_VOLUME=2875012, PRELIM_GROSS_TOO_LOW=596945, OVER_CANDIDATE_CAP=360202, NO_POSITIVE_MARGINAL_EDGE=109458
- strike_inconsistency: NO_QUOTE=531607998, LOW_VOLUME=158984367, PRELIM_GROSS_TOO_LOW=23600323, LEG_NOT_TRADABLE=9221490, OVER_CANDIDATE_CAP=283720
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
