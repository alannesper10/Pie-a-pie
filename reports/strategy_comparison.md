# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 494 (494) | 478 (478) | 478 (478) | 45 |
| Oportunidades | 77334 | 71540 | 70351 | 0 |
| Net-positive | 2 | 0 | 1 | 0 |
| Ejecutables | 2 | 0 | 0 | 0 |
| Descartadas | 77332 | 6872428 | 469553146 | 2412 |
| Duración media (min) | 0 | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.004 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05578 | 0.04313 | 0.02135 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 1 | n/d |
| Oport. por ciclo | 156.5 | 149.7 | 147.2 | n/d |
| Caja paper US$ | 81.24 | 100 | 100 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 0 | 0 |
| Fees paper US$ | 1.18 | 0 | 0 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=77263, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=4252746, LOW_VOLUME=1857087, PRELIM_GROSS_TOO_LOW=388764, OVER_CANDIDATE_CAP=231595, NO_POSITIVE_MARGINAL_EDGE=71667
- strike_inconsistency: NO_QUOTE=350630996, LOW_VOLUME=98092318, PRELIM_GROSS_TOO_LOW=14483961, LEG_NOT_TRADABLE=5964771, GROUPING_MISMATCH=155380
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
