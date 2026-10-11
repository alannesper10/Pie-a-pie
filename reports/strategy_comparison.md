# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 271 (271) | 255 (255) | 255 (255) | 45 |
| Oportunidades | 48147 | 38164 | 37425 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 48147 | 3812391 | 252672468 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.012 | 2.094 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05543 | 0.04401 | 0.02204 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0 | 1 | n/d |
| Oport. por ciclo | 177.7 | 149.7 | 146.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=48147
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2390195, LOW_VOLUME=1002136, PRELIM_GROSS_TOO_LOW=214434, OVER_CANDIDATE_CAP=126872, NO_POSITIVE_MARGINAL_EDGE=38234
- strike_inconsistency: NO_QUOTE=187638831, LOW_VOLUME=53125290, PRELIM_GROSS_TOO_LOW=8335367, LEG_NOT_TRADABLE=3369060, GROUPING_MISMATCH=83405
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
