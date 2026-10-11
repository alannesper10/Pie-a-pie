# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 281 (281) | 265 (265) | 265 (265) | 45 |
| Oportunidades | 49530 | 39662 | 38818 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 49530 | 3942251 | 262284960 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.084 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05547 | 0.0439 | 0.02199 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 176.3 | 149.7 | 146.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=49530
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2473093, LOW_VOLUME=1034663, PRELIM_GROSS_TOO_LOW=222151, OVER_CANDIDATE_CAP=130463, NO_POSITIVE_MARGINAL_EDGE=39731
- strike_inconsistency: NO_QUOTE=195037257, LOW_VOLUME=54977530, PRELIM_GROSS_TOO_LOW=8602154, LEG_NOT_TRADABLE=3455097, GROUPING_MISMATCH=86727
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
