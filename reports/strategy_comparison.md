# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 212 (212) | 196 (196) | 196 (196) | 45 |
| Oportunidades | 36360 | 29336 | 28828 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 36360 | 2987646 | 193348787 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.013 | 2.141 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05494 | 0.04466 | 0.0221 | 0.004261 |
| Tamaño disponible (máx) | 0.03 | 0 | 1 | n/d |
| Oport. por ciclo | 171.5 | 149.7 | 147.1 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=36360
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=1868996, LOW_VOLUME=792147, PRELIM_GROSS_TOO_LOW=165259, OVER_CANDIDATE_CAP=101257, NO_POSITIVE_MARGINAL_EDGE=29388
- strike_inconsistency: NO_QUOTE=142350083, LOW_VOLUME=41238677, PRELIM_GROSS_TOO_LOW=6643396, LEG_NOT_TRADABLE=2954025, OVER_CANDIDATE_CAP=68610
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
