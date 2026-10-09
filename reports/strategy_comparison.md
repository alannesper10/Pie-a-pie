# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 128 (128) | 112 (112) | 112 (112) | 45 |
| Oportunidades | 18134 | 16765 | 16550 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 18134 | 1659806 | 108850592 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.174 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.0543 | 0.04519 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 141.7 | 149.7 | 147.8 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=18134
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1026594, LOW_VOLUME=455295, PRELIM_GROSS_TOO_LOW=90093, OVER_CANDIDATE_CAP=54629, NO_POSITIVE_MARGINAL_EDGE=16793
- strike_inconsistency: NO_QUOTE=81731178, LOW_VOLUME=22077735, PRELIM_GROSS_TOO_LOW=3437433, LEG_NOT_TRADABLE=1514438, GROUPING_MISMATCH=36771
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
