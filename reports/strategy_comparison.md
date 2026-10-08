# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 22 (22) | 6 (6) | 6 (6) | 45 |
| Oportunidades | 2712 | 897 | 894 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2712 | 82921 | 6562143 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.578 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05505 | 0.04909 | 0.02161 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.3 | 149.5 | 149 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2712
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=50797, LOW_VOLUME=23158, PRELIM_GROSS_TOO_LOW=4437, OVER_CANDIDATE_CAP=2796, NO_POSITIVE_MARGINAL_EDGE=900
- strike_inconsistency: NO_QUOTE=5100362, LOW_VOLUME=1234694, PRELIM_GROSS_TOO_LOW=187352, LEG_NOT_TRADABLE=34699, OVER_CANDIDATE_CAP=2126
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
