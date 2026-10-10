# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 166 (166) | 150 (150) | 150 (150) | 45 |
| Oportunidades | 26234 | 22454 | 22121 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 26234 | 2268865 | 145716669 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.156 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05479 | 0.04505 | 0.02196 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 158 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=26234
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1411155, LOW_VOLUME=612552, PRELIM_GROSS_TOO_LOW=123797, OVER_CANDIDATE_CAP=76166, NO_POSITIVE_MARGINAL_EDGE=22491
- strike_inconsistency: NO_QUOTE=107857634, LOW_VOLUME=30891803, PRELIM_GROSS_TOO_LOW=4809666, LEG_NOT_TRADABLE=2035250, OVER_CANDIDATE_CAP=50395
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
