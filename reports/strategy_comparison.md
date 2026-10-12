# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 320 (320) | 304 (304) | 304 (304) | 45 |
| Oportunidades | 54762 | 45499 | 44569 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 54762 | 4428133 | 301064953 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.065 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04368 | 0.02182 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171.1 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=54762
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2776011, LOW_VOLUME=1162620, PRELIM_GROSS_TOO_LOW=249451, OVER_CANDIDATE_CAP=146013, NO_POSITIVE_MARGINAL_EDGE=45576
- strike_inconsistency: NO_QUOTE=226033473, LOW_VOLUME=61651287, PRELIM_GROSS_TOO_LOW=9400177, LEG_NOT_TRADABLE=3740707, GROUPING_MISMATCH=98889
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
