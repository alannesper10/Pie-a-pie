# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 193 (193) | 177 (177) | 177 (177) | 45 |
| Oportunidades | 32678 | 26493 | 26149 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 32678 | 2697675 | 173947906 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.137 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0549 | 0.04468 | 0.02217 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 169.3 | 149.7 | 147.7 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=32678
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1683654, LOW_VOLUME=720291, PRELIM_GROSS_TOO_LOW=148292, OVER_CANDIDATE_CAP=91769, NO_POSITIVE_MARGINAL_EDGE=26539
- strike_inconsistency: NO_QUOTE=128240429, LOW_VOLUME=37110437, PRELIM_GROSS_TOO_LOW=5833330, LEG_NOT_TRADABLE=2620309, OVER_CANDIDATE_CAP=58601
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
