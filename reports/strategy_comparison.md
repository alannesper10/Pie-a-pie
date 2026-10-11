# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 234 (234) | 218 (218) | 218 (218) | 45 |
| Oportunidades | 40456 | 32622 | 31957 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 40456 | 3305647 | 215621938 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.133 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05505 | 0.0445 | 0.02203 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 172.9 | 149.6 | 146.6 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=40456
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=2069446, LOW_VOLUME=874016, PRELIM_GROSS_TOO_LOW=183720, OVER_CANDIDATE_CAP=110894, NO_POSITIVE_MARGINAL_EDGE=32686
- strike_inconsistency: NO_QUOTE=159248824, LOW_VOLUME=45747109, PRELIM_GROSS_TOO_LOW=7329903, LEG_NOT_TRADABLE=3115399, OVER_CANDIDATE_CAP=76078
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
