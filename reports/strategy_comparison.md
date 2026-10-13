# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 369 (369) | 353 (353) | 353 (353) | 45 |
| Oportunidades | 61005 | 52836 | 51861 | 0 |
| Net-positive | 2 | 0 | 0 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 61003 | 5072069 | 346500653 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.045 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05606 | 0.04352 | 0.02161 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 165.3 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=60953, SUSPICIOUS_EDGE_CHECK_RULES=50
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3166233, LOW_VOLUME=1343432, PRELIM_GROSS_TOO_LOW=285693, OVER_CANDIDATE_CAP=168824, NO_POSITIVE_MARGINAL_EDGE=52923
- strike_inconsistency: NO_QUOTE=260978444, LOW_VOLUME=70215542, PRELIM_GROSS_TOO_LOW=10612231, LEG_NOT_TRADABLE=4418836, GROUPING_MISMATCH=115134
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
