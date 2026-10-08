# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 61 (61) | 45 (45) | 45 (45) | 45 |
| Oportunidades | 6816 | 6737 | 6670 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 6816 | 632199 | 45091279 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.317 | 1.034 | 59.49 |
| Fees por oportunidad (media) | 0.05427 | 0.04653 | 0.02248 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 111.7 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=6816
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=384818, LOW_VOLUME=178869, PRELIM_GROSS_TOO_LOW=35540, OVER_CANDIDATE_CAP=19761, NO_POSITIVE_MARGINAL_EDGE=6747
- strike_inconsistency: NO_QUOTE=34518416, LOW_VOLUME=8634875, PRELIM_GROSS_TOO_LOW=1340172, LEG_NOT_TRADABLE=563112, GROUPING_MISMATCH=14752
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
