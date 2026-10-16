# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 489 (489) | 473 (473) | 473 (473) | 45 |
| Oportunidades | 76450 | 70793 | 69601 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 76448 | 6795300 | 464203309 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.004 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05578 | 0.04313 | 0.02136 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.3 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=76379, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4205314, LOW_VOLUME=1836068, PRELIM_GROSS_TOO_LOW=384282, OVER_CANDIDATE_CAP=228767, NO_POSITIVE_MARGINAL_EDGE=70917
- strike_inconsistency: NO_QUOTE=346711082, LOW_VOLUME=96875975, PRELIM_GROSS_TOO_LOW=14318494, LEG_NOT_TRADABLE=5921281, GROUPING_MISMATCH=153778
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
