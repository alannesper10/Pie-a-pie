# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 322 (322) | 306 (306) | 306 (306) | 45 |
| Oportunidades | 55066 | 45799 | 44867 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 55066 | 4453278 | 302913384 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.063 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05561 | 0.04367 | 0.02181 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 171 | 149.7 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=55066
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2791636, LOW_VOLUME=1169295, PRELIM_GROSS_TOO_LOW=250899, OVER_CANDIDATE_CAP=146843, NO_POSITIVE_MARGINAL_EDGE=45876
- strike_inconsistency: NO_QUOTE=227501019, LOW_VOLUME=61968678, PRELIM_GROSS_TOO_LOW=9448617, LEG_NOT_TRADABLE=3754421, GROUPING_MISMATCH=99507
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
