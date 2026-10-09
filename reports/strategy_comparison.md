# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 84 (84) | 68 (68) | 68 (68) | 45 |
| Oportunidades | 10050 | 10181 | 10081 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 10050 | 978010 | 65139170 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.206 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05412 | 0.04556 | 0.02201 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 119.6 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=10050
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=600724, LOW_VOLUME=272649, PRELIM_GROSS_TOO_LOW=53671, OVER_CANDIDATE_CAP=31077, NO_POSITIVE_MARGINAL_EDGE=10196
- strike_inconsistency: NO_QUOTE=48789662, LOW_VOLUME=13244469, PRELIM_GROSS_TOO_LOW=2086437, LEG_NOT_TRADABLE=964259, GROUPING_MISMATCH=22392
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
