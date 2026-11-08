# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 906 (906) | 890 (889) | 890 (889) | 45 |
| Oportunidades | 142690 | 133045 | 130928 | 0 |
| Net-positive | 2 | 0 | 48 | 0 |
| Ejecutables | 2 | 0 | 44 | 0 |
| Descartadas | 142688 | 13307332 | 934177274 | 2412 |
| Duración media (min) | 0 | n/d | 18.44 | n/d |
| Capital por paquete (media) | 1.014 | 1.934 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05505 | 0.04219 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 637.3 | n/d |
| Oport. por ciclo | 157.5 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=142619, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8070373, LOW_VOLUME=3770395, PRELIM_GROSS_TOO_LOW=748225, OVER_CANDIDATE_CAP=453650, NO_POSITIVE_MARGINAL_EDGE=133297
- strike_inconsistency: NO_QUOTE=686061006, LOW_VOLUME=205177725, PRELIM_GROSS_TOO_LOW=29856129, LEG_NOT_TRADABLE=12266450, OVER_CANDIDATE_CAP=391312
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
