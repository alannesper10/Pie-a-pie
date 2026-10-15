# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 463 (463) | 447 (447) | 447 (447) | 45 |
| Oportunidades | 72483 | 66903 | 65783 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 72481 | 6397078 | 438505217 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.01 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05585 | 0.04316 | 0.02141 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.6 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=72412, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=3960376, LOW_VOLUME=1725497, PRELIM_GROSS_TOO_LOW=362657, OVER_CANDIDATE_CAP=215307, NO_POSITIVE_MARGINAL_EDGE=67019
- strike_inconsistency: NO_QUOTE=328907578, LOW_VOLUME=90071909, PRELIM_GROSS_TOO_LOW=13461313, LEG_NOT_TRADABLE=5711199, GROUPING_MISMATCH=145475
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
