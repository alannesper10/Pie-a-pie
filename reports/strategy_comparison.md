# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 297 (297) | 281 (281) | 281 (281) | 45 |
| Oportunidades | 51510 | 42056 | 41135 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 51510 | 4142349 | 278217240 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.074 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05555 | 0.04379 | 0.0219 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 173.4 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=51510
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2598435, LOW_VOLUME=1087001, PRELIM_GROSS_TOO_LOW=233328, OVER_CANDIDATE_CAP=136421, NO_POSITIVE_MARGINAL_EDGE=42127
- strike_inconsistency: NO_QUOTE=207710179, LOW_VOLUME=57777328, PRELIM_GROSS_TOO_LOW=8924924, LEG_NOT_TRADABLE=3580326, GROUPING_MISMATCH=91782
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
