# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 222 (222) | 206 (206) | 206 (206) | 45 |
| Oportunidades | 38224 | 30828 | 30257 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 38224 | 3134833 | 203574394 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.138 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05496 | 0.04459 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.2 | 149.7 | 146.9 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=38224
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1962436, LOW_VOLUME=829131, PRELIM_GROSS_TOO_LOW=174003, OVER_CANDIDATE_CAP=105699, NO_POSITIVE_MARGINAL_EDGE=30886
- strike_inconsistency: NO_QUOTE=150028311, LOW_VOLUME=43346418, PRELIM_GROSS_TOO_LOW=6998504, LEG_NOT_TRADABLE=3029171, OVER_CANDIDATE_CAP=73153
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
