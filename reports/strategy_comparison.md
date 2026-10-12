# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 331 (331) | 315 (315) | 315 (315) | 45 |
| Oportunidades | 56404 | 47147 | 46212 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 56404 | 4567272 | 309479340 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.056 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05563 | 0.04361 | 0.02176 | 0.004261 |
| Tamaño disponible (máx) | 56 | 0.1 | 1 | n/d |
| Oport. por ciclo | 170.4 | 149.7 | 146.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=56402, SUSPICIOUS_EDGE_CHECK_RULES=2
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2862366, LOW_VOLUME=1199480, PRELIM_GROSS_TOO_LOW=257622, OVER_CANDIDATE_CAP=150661, NO_POSITIVE_MARGINAL_EDGE=47226
- strike_inconsistency: NO_QUOTE=232365380, LOW_VOLUME=63373521, PRELIM_GROSS_TOO_LOW=9670451, LEG_NOT_TRADABLE=3823121, GROUPING_MISMATCH=102449
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
