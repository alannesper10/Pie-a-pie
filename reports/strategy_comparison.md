# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 130 (130) | 114 (114) | 114 (114) | 45 |
| Oportunidades | 18544 | 17063 | 16849 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 18544 | 1691535 | 110175068 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.174 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05432 | 0.0452 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 142.6 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=18544
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1046742, LOW_VOLUME=463492, PRELIM_GROSS_TOO_LOW=91817, OVER_CANDIDATE_CAP=55707, NO_POSITIVE_MARGINAL_EDGE=17092
- strike_inconsistency: NO_QUOTE=82349448, LOW_VOLUME=22438192, PRELIM_GROSS_TOO_LOW=3505673, LEG_NOT_TRADABLE=1790361, GROUPING_MISMATCH=37421
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
