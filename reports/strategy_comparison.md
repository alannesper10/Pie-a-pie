# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 917 (917) | 901 (900) | 901 (900) | 45 |
| Oportunidades | 143921 | 134693 | 132560 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 143919 | 13522855 | 948982743 | 2412 |
| Duración media (min) | 0 | n/d | 16.13 | n/d |
| Capital por paquete (media) | 1.014 | 1.929 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05501 | 0.04216 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 156.9 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=143850, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8163326, LOW_VOLUME=3876342, PRELIM_GROSS_TOO_LOW=757593, OVER_CANDIDATE_CAP=456783, NO_POSITIVE_MARGINAL_EDGE=134947
- strike_inconsistency: NO_QUOTE=697619440, LOW_VOLUME=207775102, PRELIM_GROSS_TOO_LOW=30187370, LEG_NOT_TRADABLE=12573373, OVER_CANDIDATE_CAP=397228
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
