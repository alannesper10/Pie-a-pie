# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 112 (112) | 96 (96) | 96 (96) | 45 |
| Oportunidades | 14850 | 14375 | 14210 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 14850 | 1408810 | 94429611 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.186 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05411 | 0.04525 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 132.6 | 149.7 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=14850
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=867752, LOW_VOLUME=390033, PRELIM_GROSS_TOO_LOW=76297, OVER_CANDIDATE_CAP=46043, NO_POSITIVE_MARGINAL_EDGE=14395
- strike_inconsistency: NO_QUOTE=71231137, LOW_VOLUME=19061865, PRELIM_GROSS_TOO_LOW=2911057, LEG_NOT_TRADABLE=1148769, GROUPING_MISMATCH=31571
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
