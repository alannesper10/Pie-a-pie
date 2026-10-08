# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 76 (76) | 60 (60) | 60 (60) | 45 |
| Oportunidades | 8838 | 8984 | 8893 | 0 |
| Net-positive | 0 | 0 | 0 | 0 |
| Ejecutables | 0 | 0 | 0 | 0 |
| Descartadas | 8838 | 855695 | 56732360 | 2412 |
| Duración media (min) | n/d | n/d | n/d | n/d |
| Capital por paquete (media) | 1.015 | 2.253 | 1.033 | 59.49 |
| Fees por oportunidad (media) | 0.05423 | 0.04595 | 0.02217 | 0.004261 |
| Tamaño disponible (máx) | 0 | 0 | 1 | n/d |
| Oport. por ciclo | 116.3 | 149.7 | 148.2 | n/d |
| Caja paper US$ | 100 | 100 | 100 | 100 |
| Capital bloqueado US$ | 0 | 0 | 0 | 0 |
| Fees paper US$ | 0 | 0 | 0 | 0 |
| Slippage paper US$ | 0 | 0 | 0 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=8838
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=524092, LOW_VOLUME=239868, PRELIM_GROSS_TOO_LOW=47252, OVER_CANDIDATE_CAP=27055, NO_POSITIVE_MARGINAL_EDGE=8997
- strike_inconsistency: NO_QUOTE=42414434, LOW_VOLUME=11542067, PRELIM_GROSS_TOO_LOW=1815587, LEG_NOT_TRADABLE=913011, GROUPING_MISMATCH=19732
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
