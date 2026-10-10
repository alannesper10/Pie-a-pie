# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 151 (151) | 135 (135) | 135 (135) | 45 |
| Oportunidades | 22678 | 20208 | 19926 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 22678 | 2027630 | 130243262 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.17 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05459 | 0.04522 | 0.02187 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 150.2 | 149.7 | 147.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=22678
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1259932, LOW_VOLUME=550006, PRELIM_GROSS_TOO_LOW=110421, OVER_CANDIDATE_CAP=67187, NO_POSITIVE_MARGINAL_EDGE=20241
- strike_inconsistency: NO_QUOTE=96590212, LOW_VOLUME=27340616, PRELIM_GROSS_TOO_LOW=4276933, LEG_NOT_TRADABLE=1924955, OVER_CANDIDATE_CAP=45780
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
