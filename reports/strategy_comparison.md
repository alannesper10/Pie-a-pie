# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 203 (203) | 187 (187) | 187 (187) | 45 |
| Oportunidades | 34649 | 27989 | 27580 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 34649 | 2851820 | 184452492 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.138 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05491 | 0.04467 | 0.02215 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 170.7 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=34649
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1782258, LOW_VOLUME=758193, PRELIM_GROSS_TOO_LOW=157448, OVER_CANDIDATE_CAP=97024, NO_POSITIVE_MARGINAL_EDGE=28039
- strike_inconsistency: NO_QUOTE=135879719, LOW_VOLUME=39301145, PRELIM_GROSS_TOO_LOW=6275635, LEG_NOT_TRADABLE=2842534, OVER_CANDIDATE_CAP=63819
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
