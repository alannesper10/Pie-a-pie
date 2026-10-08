# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 75 (75) | 59 (59) | 59 (59) | 45 |
| Oportunidades | 8687 | 8834 | 8746 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8687 | 840530 | 55705248 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.257 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05424 | 0.04599 | 0.0222 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 115.8 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8687
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=514587, LOW_VOLUME=235779, PRELIM_GROSS_TOO_LOW=46465, OVER_CANDIDATE_CAP=26563, NO_POSITIVE_MARGINAL_EDGE=8847
- strike_inconsistency: NO_QUOTE=41634127, LOW_VOLUME=11334009, PRELIM_GROSS_TOO_LOW=1783960, LEG_NOT_TRADABLE=906764, GROUPING_MISMATCH=19400
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
