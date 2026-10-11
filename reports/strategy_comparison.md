# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 232 (232) | 216 (216) | 216 (216) | 45 |
| Oportunidades | 40064 | 32323 | 31664 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 40064 | 3277570 | 213631239 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.135 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05503 | 0.04453 | 0.02202 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.7 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=40064
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2051910, LOW_VOLUME=866612, PRELIM_GROSS_TOO_LOW=182117, OVER_CANDIDATE_CAP=110016, NO_POSITIVE_MARGINAL_EDGE=32386
- strike_inconsistency: NO_QUOTE=157723034, LOW_VOLUME=45347563, PRELIM_GROSS_TOO_LOW=7279329, LEG_NOT_TRADABLE=3101830, OVER_CANDIDATE_CAP=75812
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
