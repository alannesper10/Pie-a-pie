# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 287 (287) | 271 (271) | 271 (271) | 45 |
| Oportunidades | 50290 | 40556 | 39693 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 50290 | 4017353 | 268253880 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.08 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0555 | 0.04386 | 0.02195 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 175.2 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=50290
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2520525, LOW_VOLUME=1053922, PRELIM_GROSS_TOO_LOW=226460, OVER_CANDIDATE_CAP=132604, NO_POSITIVE_MARGINAL_EDGE=40627
- strike_inconsistency: NO_QUOTE=199760546, LOW_VOLUME=56042801, PRELIM_GROSS_TOO_LOW=8728891, LEG_NOT_TRADABLE=3503897, GROUPING_MISMATCH=88661
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
