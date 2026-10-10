# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 167 (167) | 151 (151) | 151 (151) | 45 |
| Oportunidades | 26484 | 22604 | 22270 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 26484 | 2284835 | 146756716 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.014 | 2.156 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05481 | 0.04505 | 0.02198 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 158.6 | 149.7 | 147.5 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=26484
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1421180, LOW_VOLUME=616661, PRELIM_GROSS_TOO_LOW=124706, OVER_CANDIDATE_CAP=76776, NO_POSITIVE_MARGINAL_EDGE=22641
- strike_inconsistency: NO_QUOTE=108606486, LOW_VOLUME=31125283, PRELIM_GROSS_TOO_LOW=4845096, LEG_NOT_TRADABLE=2056799, OVER_CANDIDATE_CAP=50654
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
