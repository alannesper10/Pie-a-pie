# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 139 (139) | 123 (123) | 123 (123) | 45 |
| Oportunidades | 20202 | 18410 | 18183 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 20202 | 1834527 | 117742954 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.183 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05442 | 0.04534 | 0.02191 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 145.3 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=20202
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1137620, LOW_VOLUME=500494, PRELIM_GROSS_TOO_LOW=99670, OVER_CANDIDATE_CAP=60359, NO_POSITIVE_MARGINAL_EDGE=18441
- strike_inconsistency: NO_QUOTE=87564288, LOW_VOLUME=24416737, PRELIM_GROSS_TOO_LOW=3815392, LEG_NOT_TRADABLE=1848015, GROUPING_MISMATCH=40346
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
