# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 101 (101) | 85 (85) | 85 (85) | 45 |
| Oportunidades | 12785 | 12729 | 12570 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 12785 | 1240082 | 82884378 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.187 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04532 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 126.6 | 149.8 | 147.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=12785
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=763040, LOW_VOLUME=344524, PRELIM_GROSS_TOO_LOW=67177, OVER_CANDIDATE_CAP=39902, NO_POSITIVE_MARGINAL_EDGE=12746
- strike_inconsistency: NO_QUOTE=62309823, LOW_VOLUME=16843670, PRELIM_GROSS_TOO_LOW=2583067, LEG_NOT_TRADABLE=1079136, GROUPING_MISMATCH=27996
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
