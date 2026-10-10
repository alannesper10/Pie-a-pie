# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 182 (182) | 166 (166) | 166 (166) | 45 |
| Oportunidades | 30160 | 24847 | 24511 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 30160 | 2523377 | 162385500 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.147 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04483 | 0.02211 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 165.7 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=30160
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1571979, LOW_VOLUME=677406, PRELIM_GROSS_TOO_LOW=138323, OVER_CANDIDATE_CAP=85556, NO_POSITIVE_MARGINAL_EDGE=24889
- strike_inconsistency: NO_QUOTE=119880527, LOW_VOLUME=34599998, PRELIM_GROSS_TOO_LOW=5390060, LEG_NOT_TRADABLE=2380417, OVER_CANDIDATE_CAP=54945
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
