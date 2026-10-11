# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 236 (236) | 220 (220) | 220 (220) | 45 |
| Oportunidades | 40858 | 32921 | 32254 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 40858 | 3333603 | 217611878 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.131 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05508 | 0.04447 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 173.1 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=40858
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2086935, LOW_VOLUME=881353, PRELIM_GROSS_TOO_LOW=185321, OVER_CANDIDATE_CAP=111806, NO_POSITIVE_MARGINAL_EDGE=32986
- strike_inconsistency: NO_QUOTE=160773821, LOW_VOLUME=46146186, PRELIM_GROSS_TOO_LOW=7380890, LEG_NOT_TRADABLE=3129035, OVER_CANDIDATE_CAP=76367
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
