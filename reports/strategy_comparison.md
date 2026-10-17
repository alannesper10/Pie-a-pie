# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 534 (534) | 518 (518) | 518 (518) | 45 |
| Oportunidades | 85789 | 77524 | 76312 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 85787 | 7517596 | 509345652 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 1.999 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05565 | 0.04309 | 0.02127 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 160.7 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=85718, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4657329, LOW_VOLUME=2026516, PRELIM_GROSS_TOO_LOW=424425, OVER_CANDIDATE_CAP=256165, NO_POSITIVE_MARGINAL_EDGE=77664
- strike_inconsistency: NO_QUOTE=377407715, LOW_VOLUME=108836855, PRELIM_GROSS_TOO_LOW=16104760, LEG_NOT_TRADABLE=6572620, OVER_CANDIDATE_CAP=176528
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
