# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 107 (107) | 91 (91) | 91 (91) | 45 |
| Oportunidades | 13884 | 13628 | 13468 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 13884 | 1332090 | 89175389 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.184 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0541 | 0.04524 | 0.02189 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 129.8 | 149.8 | 148 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=13884
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=820097, LOW_VOLUME=369398, PRELIM_GROSS_TOO_LOW=72164, OVER_CANDIDATE_CAP=43229, NO_POSITIVE_MARGINAL_EDGE=13646
- strike_inconsistency: NO_QUOTE=67166322, LOW_VOLUME=18057067, PRELIM_GROSS_TOO_LOW=2761567, LEG_NOT_TRADABLE=1117335, GROUPING_MISMATCH=29946
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
