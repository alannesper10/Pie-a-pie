# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 180 (180) | 164 (164) | 164 (164) | 45 |
| Oportunidades | 29681 | 24548 | 24211 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 29681 | 2491536 | 160292733 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.147 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05493 | 0.04486 | 0.0221 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 164.9 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=29681
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1551698, LOW_VOLUME=669394, PRELIM_GROSS_TOO_LOW=136519, OVER_CANDIDATE_CAP=84426, NO_POSITIVE_MARGINAL_EDGE=24590
- strike_inconsistency: NO_QUOTE=118371059, LOW_VOLUME=34136394, PRELIM_GROSS_TOO_LOW=5315235, LEG_NOT_TRADABLE=2337088, OVER_CANDIDATE_CAP=54358
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
