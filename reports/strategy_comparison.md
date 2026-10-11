# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 235 (235) | 219 (219) | 219 (219) | 45 |
| Oportunidades | 40651 | 32772 | 32105 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 40651 | 3319629 | 216616923 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.131 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05506 | 0.04448 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 173 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=40651
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2078191, LOW_VOLUME=877695, PRELIM_GROSS_TOO_LOW=184519, OVER_CANDIDATE_CAP=111344, NO_POSITIVE_MARGINAL_EDGE=32836
- strike_inconsistency: NO_QUOTE=160011183, LOW_VOLUME=45946863, PRELIM_GROSS_TOO_LOW=7355363, LEG_NOT_TRADABLE=3122207, OVER_CANDIDATE_CAP=76205
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
