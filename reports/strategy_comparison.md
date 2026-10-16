# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 509 (509) | 493 (493) | 493 (493) | 45 |
| Oportunidades | 80439 | 73787 | 72595 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 80437 | 7110064 | 483624757 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.001 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05574 | 0.0431 | 0.02132 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 158 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=80368, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4401291, LOW_VOLUME=1919865, PRELIM_GROSS_TOO_LOW=402242, OVER_CANDIDATE_CAP=240471, NO_POSITIVE_MARGINAL_EDGE=73917
- strike_inconsistency: NO_QUOTE=360389864, LOW_VOLUME=101483550, PRELIM_GROSS_TOO_LOW=15008179, LEG_NOT_TRADABLE=6347876, GROUPING_MISMATCH=160244
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
