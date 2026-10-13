# Laboratorio Pie a Pie — replay-collect-final-s7-161723

Modo: replay · inicio 2026-10-13T19:17:23.014+00:00 · semilla 7 · replay de collect-final

Todo es SIMULADO. OBSERVADO = datos públicos crudos; ESTIMADO = neto con costos modelados; SIMULADO = ejecución con latencia, fills parciales y liquidez compartida.

## Comparación por estrategia

| Estrategia | Observadas | Estimadas > 0 | Ejecutadas (sim) | Rentables (sim) | Neto sim. | Capital comprometido | Retorno s/ capital | Peor/mejor (p5/p95) | Veredicto |
|---|---|---|---|---|---|---|---|---|---|
| calendar_spread | 756 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **ESTADISTICA: SIN EVIDENCIA SUFICIENTE (no es arbitraje)** |
| cash_and_carry | 1080 | 309 | 1 | 1 | US$+0.2379 | US$90.39 | 0.263% | 0.263% / 0.263% | **SIN EVIDENCIA SUFICIENTE** |
| cex_dex | 1500 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |
| cross_exchange | 780 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |
| liquidity_provision | 203 | 0 | 203 | 4 | US$-2.6038 | US$4060.00 | -0.064% | -0.110% / -0.021% | **ESTADISTICA: NO RENTABLE (no es arbitraje)** |
| polymarket_buy_all_no | 1646 | 1 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |
| prediction_cross_venue | 0 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **NO VERIFICABLE** |
| triangular | 695 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |

**Consolidado:** 8 estrategias, capital US$800 (separado), ejecutadas 204, rentables 5, neto simulado US$-2.3659, realizado en ledgers US$-2.3955.

## Por categoría pedida

- **1. Entre exchanges (cripto)** — cross_exchange: SIN EVIDENCIA SUFICIENTE
- **2. Basis spot-futuros / funding** — no corrió en esta ejecución
- **3. Triangular** — triangular: SIN EVIDENCIA SUFICIENTE
- **4. Mercados de predicción** — polymarket_buy_all_no: SIN EVIDENCIA SUFICIENTE; prediction_cross_venue: NO VERIFICABLE
- **5. Provisión de liquidez** — liquidity_provision: ESTADISTICA: NO RENTABLE (no es arbitraje)

## Evidencia externa (no recalculada)

- kalshi_current: source=data/ (GitHub Actions, solo lectura), cycles=386, opportunities=63114, net_positive=2, executable=2, pnl_realized=0
- buy_all_no: source=data/ (GitHub Actions, solo lectura), cycles=370, opportunities=55381, net_positive=0, executable=0, pnl_realized=0
- strike_inconsistency: source=data/ (GitHub Actions, solo lectura), cycles=370, opportunities=54392, net_positive=0, executable=0, pnl_realized=0
- funding_phase0: source=reports\funding_basis, phase0_decisions=2412, cycles=45, opportunities=0, net_positive=0, executable=0, pnl_realized=0.0

## Detalle

### calendar_spread

- Veredicto: **ESTADISTICA: SIN EVIDENCIA SUFICIENTE (no es arbitraje)** — neto simulado +0.0000 USD; 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: OBSERVATION_NO_MODEL=756
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'calendar_spread', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### cash_and_carry

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 1 ejecuciones simuladas (mín 30), 1 períodos (mín 6)
- Motivos: NET_NEGATIVE_AFTER_COSTS=605, INFEASIBLE_MIN_SIZE=324, NO_CAPITAL=150, FILLED=1
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): {'p5': 2, 'p25': 4, 'p50': 6, 'p75': 27, 'p95': 54, 'mean': 20.6, 'std': 21.47805081162317, 'n': 15}
- Períodos (10 min): 1, positivos 100%
- Estrés x1.5: estimadas > 0 255, neto sim. US$+0.1590 · x2: 216, US$+0.0800
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 1, 'in_sample_net': 0.23790020370666212, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'cash_and_carry', 'capital': 100.0, 'cash': 9.610141396389196, 'locked': 90.3898586036108, 'peak_locked': 90.3898586036108, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### cex_dex

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NET_NEGATIVE_AFTER_COSTS=1500
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 26, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'cex_dex', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### cross_exchange

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NO_EDGE_AFTER_FEES=774, STALE_BOOKS=6
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'cross_exchange', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### liquidity_provision

- Veredicto: **ESTADISTICA: NO RENTABLE (no es arbitraje)** — neto simulado -2.6038 USD; neto > 0: no, fuera de muestra > 0: no, estrés x1.5 > 0: no, períodos positivos >= 60%: no
- Motivos: FILL=203
- Pérdidas: 199 (US$-2.6074)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 6, positivos 0%
- Estrés x1.5: estimadas > 0 0, neto sim. US$-3.6188 · x2: 0, US$-4.6338
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 101, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'liquidity_provision', 'capital': 100.0, 'cash': 97.60453825934356, 'locked': 0.0, 'peak_locked': 60.0, 'realized': -2.395461740656444, 'trades': 1, 'return_on_capital': -0.02395461740656444}

### polymarket_buy_all_no

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NO_EDGE_AFTER_FEES_OR_MIN_SIZE=826, NO_BOOK_FOR_LEG=559, BUDGET_TOO_SMALL=261
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): {'p5': 1, 'p25': 1, 'p50': 1, 'p75': 1, 'p95': 1, 'mean': 1, 'std': 0.0, 'n': 1}
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'polymarket_buy_all_no', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### prediction_cross_venue

- Veredicto: **NO VERIFICABLE** — sin pares verificados a mano
- Motivos: ninguno
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'status': 'INSUFICIENTES_TICKS'}
- Ledger: {'strategy': 'prediction_cross_venue', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### triangular

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NET_NEGATIVE_AFTER_COSTS=695
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 27, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'triangular', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

## Errores de fuentes

Total: 42
- jupiter:SOL->USDC|10: 7
- jupiter:USDC->SOL|10: 7
- jupiter:SOL->USDC|25: 7
- jupiter:USDC->SOL|25: 7
- jupiter:SOL->USDC|45: 7
- jupiter:USDC->SOL|45: 7
