# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 81 (81) | 65 (65) | 65 (65) | 45 |
| Oportunidades | 9598 | 9734 | 9639 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 9598 | 931914 | 61985102 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.225 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05419 | 0.04571 | 0.02207 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 118.5 | 149.8 | 148.3 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=9598
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=571939, LOW_VOLUME=260216, PRELIM_GROSS_TOO_LOW=51242, OVER_CANDIDATE_CAP=29586, NO_POSITIVE_MARGINAL_EDGE=9747
- strike_inconsistency: NO_QUOTE=46399340, LOW_VOLUME=12605421, PRELIM_GROSS_TOO_LOW=1983803, LEG_NOT_TRADABLE=944942, GROUPING_MISMATCH=21392
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
