# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 430 (430) | 414 (414) | 414 (414) | 45 |
| Oportunidades | 68540 | 61962 | 60917 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 68538 | 5915409 | 404056013 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.022 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.056 | 0.04325 | 0.02145 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 159.4 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=68469, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3672295, LOW_VOLUME=1584643, PRELIM_GROSS_TOO_LOW=335221, OVER_CANDIDATE_CAP=199382, NO_POSITIVE_MARGINAL_EDGE=62070
- strike_inconsistency: NO_QUOTE=304029665, LOW_VOLUME=81886887, PRELIM_GROSS_TOO_LOW=12347455, LEG_NOT_TRADABLE=5466927, GROUPING_MISMATCH=134883
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
