# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 302 (302) | 286 (286) | 286 (286) | 45 |
| Oportunidades | 52165 | 42805 | 41876 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 52165 | 4204847 | 283186275 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.073 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05557 | 0.04377 | 0.02188 | 0.004261 |
| Tamaño disponible (máx) | 0.94 | 0.1 | 1 | n/d |
| Oport. por ciclo | 172.7 | 149.7 | 146.4 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=52165
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2637085, LOW_VOLUME=1103730, PRELIM_GROSS_TOO_LOW=236726, OVER_CANDIDATE_CAP=138525, NO_POSITIVE_MARGINAL_EDGE=42877
- strike_inconsistency: NO_QUOTE=211685088, LOW_VOLUME=58637431, PRELIM_GROSS_TOO_LOW=9020397, LEG_NOT_TRADABLE=3615636, GROUPING_MISMATCH=93327
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
