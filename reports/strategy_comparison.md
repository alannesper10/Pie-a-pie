# Comparación de estrategias (paper only)

| Métrica | kalshi_current | buy_all_no | strike_inconsistency | funding_basis |
|---|---|---|---|---|
| Ciclos (ok) | 915 (915) | 899 (898) | 899 (898) | 45 |
| Oportunidades | 143634 | 134394 | 132262 | 0 |
| Net-positive | 2 | 0 | 52 | 0 |
| Ejecutables | 2 | 0 | 48 | 0 |
| Descartadas | 143632 | 13480324 | 945929891 | 2412 |
| Duración media (min) | 0 | n/d | 16.65 | n/d |
| Capital por paquete (media) | 1.014 | 1.93 | 1.031 | 59.49 |
| Fees por oportunidad (media) | 0.05502 | 0.04216 | 0.02105 | 0.004261 |
| Tamaño disponible (máx) | 58 | 0.1 | 819.5 | n/d |
| Oport. por ciclo | 157 | 149.7 | 147.3 | n/d |
| Caja paper US$ | 81.24 | 100 | 80.46 | 100 |
| Capital bloqueado US$ | 18.76 | 0 | 19.54 | 0 |
| Fees paper US$ | 1.18 | 0 | 0.36 | 0 |
| Slippage paper US$ | 0.304 | 0 | 0.04 | n/d |
| P&L realizado US$ | 0 | 0 | 0 | 0 |

Motivos de descarte (top 5 por estrategia):
- kalshi_current: NO_POSITIVE_MARGINAL_EDGE=143563, SUSPICIOUS_EDGE_CHECK_RULES=69
- buy_all_no: NOT_MUTUALLY_EXCLUSIVE=8144517, LOW_VOLUME=3855826, PRELIM_GROSS_TOO_LOW=755826, OVER_CANDIDATE_CAP=456100, NO_POSITIVE_MARGINAL_EDGE=134647
- strike_inconsistency: NO_QUOTE=695345496, LOW_VOLUME=207099447, PRELIM_GROSS_TOO_LOW=30113563, LEG_NOT_TRADABLE=12546280, OVER_CANDIDATE_CAP=395899
- funding_basis: COSTO_IDA_Y_VUELTA_SUPERA_FUNDING_ESPERADO=2412, INFEASIBLE_MIN_SIZE_100USD_PAIRS=2
- nota kalshi_current: los descartes del prefiltro de kalshi_current no se registran (no se modificó su código); solo se cuentan los evaluados
