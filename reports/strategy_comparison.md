# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 74 (74) | 58 (58) | 58 (58) | 45 |
| Oportunidades | 8543 | 8684 | 8596 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8543 | 825363 | 54678136 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.264 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05424 | 0.04605 | 0.02221 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 115.4 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8543
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=505085, LOW_VOLUME=231681, PRELIM_GROSS_TOO_LOW=45687, OVER_CANDIDATE_CAP=26068, NO_POSITIVE_MARGINAL_EDGE=8697
- strike_inconsistency: NO_QUOTE=40855662, LOW_VOLUME=11125235, PRELIM_GROSS_TOO_LOW=1751732, LEG_NOT_TRADABLE=899972, GROUPING_MISMATCH=19068
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
