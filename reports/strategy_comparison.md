# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 396 (396) | 380 (380) | 380 (380) | 45 |
| Oportunidades | 64271 | 56875 | 55876 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 64269 | 5437688 | 370605244 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.032 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05614 | 0.04337 | 0.02153 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 162.3 | 149.7 | 147 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=64200, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3388010, LOW_VOLUME=1446122, PRELIM_GROSS_TOO_LOW=306511, OVER_CANDIDATE_CAP=181962, NO_POSITIVE_MARGINAL_EDGE=56972
- strike_inconsistency: NO_QUOTE=279237779, LOW_VOLUME=75051961, PRELIM_GROSS_TOO_LOW=11313296, LEG_NOT_TRADABLE=4704216, GROUPING_MISMATCH=124004
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
