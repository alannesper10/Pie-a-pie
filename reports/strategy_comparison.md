# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 194 (194) | 178 (178) | 178 (178) | 45 |
| Oportunidades | 32872 | 26642 | 26293 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 32872 | 2713194 | 174999964 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.137 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04467 | 0.02218 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 169.4 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=32872
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1693594, LOW_VOLUME=724100, PRELIM_GROSS_TOO_LOW=149230, OVER_CANDIDATE_CAP=92290, NO_POSITIVE_MARGINAL_EDGE=26689
- strike_inconsistency: NO_QUOTE=129001183, LOW_VOLUME=37335327, PRELIM_GROSS_TOO_LOW=5877133, LEG_NOT_TRADABLE=2642116, OVER_CANDIDATE_CAP=58921
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
