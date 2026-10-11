# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 259 (259) | 243 (243) | 243 (243) | 45 |
| Oportunidades | 45923 | 36366 | 35680 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 45923 | 3651579 | 240593194 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.104 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05531 | 0.04414 | 0.02206 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.3 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=45923
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2287694, LOW_VOLUME=962335, PRELIM_GROSS_TOO_LOW=204521, OVER_CANDIDATE_CAP=122071, NO_POSITIVE_MARGINAL_EDGE=36434
- strike_inconsistency: NO_QUOTE=178349331, LOW_VOLUME=50783129, PRELIM_GROSS_TOO_LOW=7980634, LEG_NOT_TRADABLE=3284284, GROUPING_MISMATCH=79609
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
