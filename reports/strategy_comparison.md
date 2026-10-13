# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 362 (362) | 346 (346) | 346 (346) | 45 |
| Oportunidades | 60159 | 51787 | 50813 | 0 |
| Net-positive | 1 | 0 | 0 | 0 |
| Ejecutables | 1 | 0 | 0 | 0 |
| Descartadas | 60158 | 4977972 | 339341413 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.047 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05601 | 0.04354 | 0.02164 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 166.2 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 90.16 | 100 | 100 | 100 |
| Capital bloqueado US$ | 9.84 | 0 | 0 | 0 |
| Fees paper US$ | 0.58 | 0 | 0 | 0 |
| Slippage paper US$ | 0.16 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60114, SUSPICIOUS_EDGE_CHECK_RULES=44
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3110111, LOW_VOLUME=1316513, PRELIM_GROSS_TOO_LOW=280161, OVER_CANDIDATE_CAP=165095, NO_POSITIVE_MARGINAL_EDGE=51873
- strike_inconsistency: NO_QUOTE=255292972, LOW_VOLUME=68966337, PRELIM_GROSS_TOO_LOW=10441416, LEG_NOT_TRADABLE=4370487, GROUPING_MISMATCH=112815
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
