# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 21 (21) | 5 (5) | 5 (5) | 45 |
| Oportunidades | 2589 | 747 | 746 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 2589 | 68831 | 5464287 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.567 | 1.032 | 59.49 |
| Fees por oportunidad (media) | 0.05515 | 0.04904 | 0.02151 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 123.3 | 149.4 | 149.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=2589
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=42273, LOW_VOLUME=19112, PRELIM_GROSS_TOO_LOW=3686, OVER_CANDIDATE_CAP=2331, NO_POSITIVE_MARGINAL_EDGE=750
- strike_inconsistency: NO_QUOTE=4244500, LOW_VOLUME=1030858, PRELIM_GROSS_TOO_LOW=155705, LEG_NOT_TRADABLE=29085, OVER_CANDIDATE_CAP=1714
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
